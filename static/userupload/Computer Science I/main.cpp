#include <fstream>
#include <iostream>
#include <vector>
#include "Polynomial.h"
using namespace std;

int main( int argc, char* argv[] ) {

  if ( argc != 2 )
    {
      cerr << "Usage:  " << argv[0] << " output.txt\n";
      return 0;
    }
  ofstream out_str( argv[1] );
  if ( !out_str )
    {
      cerr << "Failed to open " << argv[1] << endl;
      return 0;
    }

  Polynomial f;
  double x = 2.5;
  double r = f.eval( x );
  int line=0;
  out_str << ++line << ":  f(" << x << ") = " << r << '\n';

  f.set_coefficient( 4, 0 );
  f.set_coefficient( 5, 3 );
  f.set_coefficient( 2, 0 );
  f.set_coefficient(-1, 1 );
  f.set_coefficient(-1, 5 );
  out_str << ++line << ":  After 5 set_coefficient calls:  f(x) = ";
  f.write( out_str );
  out_str << ++line << ":  Coefficient of x^0 is " << f.coefficient(0) << '\n';
  out_str << ++line << ":  Coefficient of x^2 is " << f.coefficient(2) << '\n';
  out_str << ++line << ":  Coefficient of x^3 is " << f.coefficient(3) << '\n';
  out_str << ++line << ":  Coefficient of x^14 is "<< f.coefficient(14)<< '\n';

  /*

  vector <int> coefficients, exponents;
  coefficients.push_back( 1 );
  coefficients.push_back( -1 ); 
  exponents.push_back( 2 );
  exponents.push_back( 0 );
  exponents.push_back( 10 ); // will be ignored
  Polynomial f1( coefficients, exponents );
  out_str << ++line << ":  f1(x) = ";
  f1.write( out_str );
  coefficients[1] = 1;
  Polynomial f2( coefficients, exponents );
  out_str << ++line << ":  f2(x) = ";
  f2.write( out_str );

  Polynomial f3 = f1.add(f2);
  out_str << ++line << ":  f1+f2 = ";
  f3.write( out_str );

  Polynomial f4 = f1.subtract(f2);
  out_str << ++line << ": f1-f2 = ";
  f4.write( out_str );

  Polynomial f5 = f1.multiply(f2);
  out_str << ++line << ": f1*f2 = ";
  f5.write( out_str );

  f1.set_coefficient( 3, 4 );
  f1.set_coefficient( 2, 5 );
  f1.set_coefficient( -8, 7 );
  out_str << ++line << ": f1(x) = ";
  f1.write( out_str );
  out_str << ++line << ": f1(2.0) = " << f1.eval(2.0) << endl;

  f2.set_coefficient( -3, 4 );
  f2.set_coefficient( 2, 5 );
  f2.set_coefficient( 1, 6 );
  f2.set_coefficient( 3, 8 );
  out_str << ++line << ": f2(x) = ";
  f2.write( out_str );

  f3 = f1.add(f2);
  out_str << ++line <<  ": f1+f2 = ";
  f3.write( out_str );

  f4 = f1.subtract(f2);
  out_str << ++line << ": f1-f2 = ";
  f4.write( out_str );

  f5 = f1.multiply(f2);
  out_str << ++line << ": f1*f2 = ";
  f5.write( out_str );

  Polynomial f6;
  f6.set_coefficient(1, 3);
  f6.set_coefficient(-5, 2);
  f6.set_coefficient(-50,1);

  out_str << ++line << ": f6(x) = ";
  f6.write( out_str );

  
  list<int> factors = f6.integer_factors();
  out_str << ++line << ": Number of factors of f6: " << factors.size() << '\n';
  if ( factors.size() > 0 )
    {
      out_str << ++line << ": Here are the factors:  ";
      for ( list<int>::iterator p = factors.begin(); p != factors.end(); ++p )
        out_str << " " << *p;
      out_str << '\n';
    }
  */
  
  return 0;
}
