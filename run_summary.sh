# all the .ctr .data file should be renamed as .err && all the .ktest file should be renamed as test0001.ktest, but not test0001.ctr.ktest
# opt -load libMackeOpt.so -preprenderror *.bc -prependtofunction functionname -errorfiletoprepend .err -o out.bc
#if there are more than one .err, just add more -errorfilrtopreprend .err -errorfilrtoprepend .err is ok
/home/jl/deploy/llvm342/Release/bin/opt -load /home/jl/deploy/macke-opt-llvm/bin/libMackeOpt.so -preprenderror /home/jl/testspace/coreutils-bc-from-use/cr-3/cut-macke-set_fields-main.bc -prependtofunction set_fields  -errorfiletoprepend /home/jl/testspace/coreutils-bc-from-use/cr-3/klee-out-3/test000001.info.ctrl.err  -o test-summary_1.bc
