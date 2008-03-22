#ifndef COMPILER_STUFF_H
#define COMPILER_STUFF_H

#ifdef __GNUC__
# define UNUSED_PARM(param) param __attribute__ ((unused))
#else
# define UNUSED_PARM(param) param
#endif

#endif /* COMPILER_STUFF_H */
