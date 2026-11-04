cd /home/claude/bench2
T(){ id=$1; shift; STDIN_FILE=${IN:-/home/claude/bench2/work/enter.in} bash run1.sh $id 0 "x" "" "[]" "$@" | tail -1 | sed "s/^/$id: /"; }
for i in 1 2 3 4 5 6; do T d1_p$i /home/claude/day1/full/p/p$i.cpp; done
T d1_dot /home/claude/day1/full/3_dot/main.cpp
S=/home/claude/day2/src
T d2_c1 $S/c1_hello.c; T d2_c2 $S/c2_malloc.c; T d2_c3 $S/c3_ptr_arith.c; T d2_c4 $S/c4_double_it.cpp
T d2_d1 $S/d1_dot_length.cpp
T d2_v1 $S/v1_basics.cpp; T d2_v2 $S/v2_loops.cpp; T d2_v3 $S/v3_full.cpp; T d2_v4 $S/v4_cad_points.cpp; T d2_v5 $S/v5_growth.cpp
S=/home/claude/day3/src
T d3_r1 $S/r1_reference.cpp; T d3_r2 $S/r2_increment.cpp; T d3_r3 $S/r3_rebind.cpp; T d3_r4 $S/r4_cherno.cpp
T d3_h1 $S/h1_hamming_strlen.c; T d3_h2 $S/h2_hamming_pointers.c; T d3_x1 $S/x1_cross.cpp
S=/home/claude/day4/src
T d4_st1 $S/st1/main.cpp $S/st1/static.cpp; T d4_st2 $S/st2/main.cpp $S/st2/static.cpp
T d4_c1 $S/c1_const_pointers.cpp; T d4_c2 $S/c2_const_method.cpp; T d4_x1 $S/x1_cross_khan.cpp
