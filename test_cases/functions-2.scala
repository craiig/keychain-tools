//testing post return state modification propagation

left=def test(x:Int): Int = { return x; }
right=def test(x:Int): Int = { return x; return x+1; }
sc.hash(test(_))

//this succeeds, so it looks to me like there is some basic optimizations being
//applied by the scala compiler!
