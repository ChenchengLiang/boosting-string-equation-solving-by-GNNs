(set-logic QF_S) 
(declare-fun A () String) 
(declare-fun B () String) 
(assert (= (str.++ "a" "a" "b" "a" "b" "b" "a" "a" "b" "b" "a" "a" "a" "a" "b" "b" "b" "a" "b" "a" "a" "a" "b" "b" "b" "b" "b" "a" "b" "b" "b" "a" "a" "b" "b" "b" "b" "a" "b" "b" "b" A "a" "a" "b" "a") (str.++ "a" "a" "b" B "b" "a" "b" "b" "a" "a" "a" "a" "b" "b" "b" "a" "a" "b" "b" "a" "b" "a" "b" "b" "a" "a" "a" "b" "b" "a" "a" "b" "a" "b" "a" "b" "a" "b" "a" "a" "b" "b" "a" "a" "b" "a" "b" "a" "b" "b" "a" "b" "a" "a" "a" "b" "b" "a" "b" "b" "a" "a" "b" "a")))
(check-sat) 
(get-model)