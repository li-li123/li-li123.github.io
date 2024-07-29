//# if (NEXT_MACG1):
#  include "god/testing/txt.c"
//# else
#if (NEXT_MACG2):
# include "god/testing/txt.c"
#else
# if (NEXT_MACG3):
# include "god/testing/txt.c"
# else
# if (NEXT_MACG4):
#  include "god/testing/txt.c"
# else