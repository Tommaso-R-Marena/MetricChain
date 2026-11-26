#!/bin/bash
# re-run the short scripts whose output was only shown on the console, saving it next to the scripts
cd "$(dirname "$0")"
python3 cmp1.py > cmp1.out 2>&1
python3 val_cpp.py > val_cpp.out 2>&1
python3 cmp5_frac.py > cmp5_frac.out 2>&1
python3 cmp4_letters.py indep > cmp4_indep.out 2>&1
python3 complexity_count.py > complexity_count.out 2>&1
python3 complexity_qs.py > complexity_qs.out 2>&1
python3 hard_models.py > hard_models.out 2>&1
python3 hard_remark5.py > hard_remark5.out 2>&1
python3 cor4_check.py > cor4_check.out 2>&1
python3 eth_no_instances.py > eth_no_instances.out 2>&1
python3 api_edge.py > api_edge.out 2>&1
python3 api_edge2.py > api_edge2.out 2>&1
echo done > rerun_save.done
