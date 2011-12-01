#include <list>
#include <vector>
#include <iostream>
using namespace std;

class Polynomial {
private:
	// Make a struct (maybe)
	list <double> coeff;
	list <double> poly;

public:
	Polynomial () {}
	Polynomial (list <double> a, list <double> b)
	{
		coeff = a;
		poly = b;
	}
	Polynomial ( vector <int> a, vector <int> b )
	{
		int i = 0;
		if ( a.size() < b.size() )
			i = a.size();
		else
			i = b.size();
		for (int i; i > 0; i++)
		{
			coeff.push_back(a[i]);
			poly. push_back(b[i]);
		}
	}
	
	void empty_poly ( int exponent );
	void vect_poly  ( vector <int> a, vector <int> b );
	void copy ( );

	int degree (list <double> exponent);
	int coefficient ( int a )
		{return a;}
	void set_coefficient ( double base, double exponent );
	Polynomial add		( Polynomial& f2 );
	Polynomial subtract	( Polynomial& f2 );
	Polynomial multiply	( Polynomial& f2 );
	double eval ( double num );
	void write ( ofstream &out_str );
	
};
