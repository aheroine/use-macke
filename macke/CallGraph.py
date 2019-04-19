"""
Class container for all call graph operations
"""

from os import path
from pprint import pformat

from . import llvm_wrapper


class CallGraph:
    """
    All information about the callgraph from a specific bitcode file
    """

    def __init__(self, bitcodefile):
        assert path.isfile(bitcodefile)
        self.graph = llvm_wrapper.extract_callgraph(bitcodefile)
        self.topology = llvm_wrapper.list_all_funcs_topological(bitcodefile)

    def __contains__(self, item):
        return item in self.graph

    def __str__(self):
        return pformat(self.graph)

    def __getitem__(self, key):
        try:
            return self.graph[key]
        except KeyError:
            return None

    def is_symbolic_encapsulable(self, function):
        """
        Checks, if a function can be encapsulated symbolically
        """
        return (not self[function]['hasdoubleptrarg'] and
                not self[function]['hasfuncptrarg'] and
                not self[function]['isexternal'])

    def get_flattened_inverted_topology(self):
        """
        Returns a sort of inverted topologically ordered list of all functions
        """
        # Nested lists of circles and SCCs are simply flattened
        flattened = []
        for topo in self.topology:
            if isinstance(topo, str):
                flattened.append(topo)
            else:
                flattened.extend(topo)
        return flattened

    def get_internal_functions(self):
        """
        Returns a list of all internal functions in arbitrary order
        """

        return [f for f, info in self.graph.items() if not info["isexternal"]]

    def list_symbolic_encapsulable(self, removemain=True):
        """
        Returns a sort of inverted topologically ordered list of all function
        names, that can be symbolically encapsulated by MACKE
        """
        flattened = self.get_flattened_inverted_topology()
        return [t for t in flattened if (self.is_symbolic_encapsulable(t) or (
            not removemain and t == "main"))]

    def group_independent_calls(self, removemain=True):
        """
        Returns a topologically ordered list of (caller, callee)-tuples
        nested in sublists, that can be analyzed in parallel processes
        """

        # Probably the result of this method is not the optimal solution
        # considering the number parallel executable pairs. But I don't
        # know a better algorithm to generate them. Maybe later ...

        units = self.group_independent_callees()

        # Convert the unit list of functions to a list of callers
        result = []
        for unit in units:
            pairs = []
            for callee in unit:
                for caller in self[callee]['calledby']:
                    if ((not removemain and caller == "main") or
                            (self.is_symbolic_encapsulable(caller))):
                        pairs.append((caller, callee))
            if pairs:
                result.append(sorted(pairs))

        # (partially) assert correctness of the result
        for res in result:
            assert res
            callers, callees = set(), set()
            for (caller, callee) in res:
                if caller != callee:
                    callers.add(caller)
                    callees.add(callee)
            assert callers.isdisjoint(callees)

        return result

    def group_independent_callees(self):
        """
        Group the topological ordered function list in independent units
        """
        units = []
        independent = set()
        earlier_calls = set()

        for topo in self.topology:
            if isinstance(topo, str):
                if topo in earlier_calls:
                    # Add all function, that are called earlier
                    if independent:
                        units.append(sorted(list(independent)))
                    # And restart the search
                    independent = set()
                    earlier_calls = set()

                # Mark this function as indepent
                independent.add(topo)
                # Mark all function called by now
                earlier_calls |= set(self[topo]['calledby'])

            else:
                # Add all previous independent functions
                if independent:
                    units.append(sorted(list(independent)))
                    independent = set()

                # Split each part of a scc in a separate run
                for arc in sorted(topo):
                    units.append([arc])

        # Add all remaining elements
        if independent:
            units.append(list(independent))

        return units

    def get_functions_with_no_caller(self):
        """
        Returns a set with all functions, that do not have any caller
        """
        return {func for func in self.get_flattened_inverted_topology()
                if not self[func]["calledby"]}
