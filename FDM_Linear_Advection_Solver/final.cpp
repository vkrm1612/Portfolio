/**
 * @file computational_methods_assignment.cpp
 * @brief Implements various numerical schemes for solving the 1-D Linear Wave Equation.
 */



#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <cmath>
#include <algorithm> 
#include <iomanip>


using namespace std;

//Declaring global variables

double c, dx, N, t;
double u=1.75;  // Velocity
double L = 100.0;  // Length 
double x_i = -50.0;  // Starting Point
double x_b = 50.0;  // Ending Point
vector<double> X; 

/**
 * @class boundary_conditions
 * @brief Initializes the initial conditions for numerical schemes.
*/


class boundary_conditions
{
public:
vector<double> set1;  ///< Vector for initial condition set 1 
vector<double> set2;  ///< Vector for boundary condition set 2

/**
* @brief Returns the sign of a given value.
* @param x Input value.
* @return -1, 0, or 1 depending on the sign of `x`.
*/
double sign(double x) {
    if (x > 0) return 1;
    else if (x < 0) return -1;
    else return 0;
}
/**
* @brief Initial condition for set 1.
* @param N Number of grid points.
* @return Vector for set 1 boundary condition.
*/
vector <double> set_1(double N)
{
    double dx = 100.0 / (N-1);
    set1.resize(N);
    int i = 0;
    for (double s_1 = x_i; s_1 < x_b+dx ; s_1 = s_1 + dx)
    {       
            set1[i] = (0.5) * (sign(s_1)+1.0);
            i = i+1;
    }   
return set1;
}

/**
* @brief Initial condition for set 2.
* @param N Number of grid points.
* @return Vector for set 2 boundary condition.
*/

vector <double> set_2(double N)
{       double dx = 100.0 / (N-1);
    set2.resize(N);
    int i=0;
    for (double s_1 = x_i; s_1 < x_b+dx ; s_1 = s_1 + dx) {
            
            set2[i] = (0.5) * exp(-s_1*s_1);
            i = i+1;
        }

    return set2;
}
};

/**
 * @class analytical_solution
 * @brief Computes analytical solutions for the wave equation.
 */

class analytical_solution
{



public:
vector<double> analytical_1; ///< Analytical solution set 1
vector<double> analytical_2; ///< Analytical solution set 2

/**
* @brief Returns the sign of a given value.
* @param x Input value.
* @return -1, 0, or 1 depending on the sign of `x`.
*/


double sign(double x) {
    if (x > 0) return 1;
    else if (x < 0) return -1;
    else return 0;
 }
/**
* @brief Computes the analytical solution for boundary condition set 1.
* @param N Number of grid points.
* @param t Time at which to compute the solution.
* @return Vector of analytical solution values for set 1.
*/
  
vector <double> analytical_set_1(double N, double t)
{


double dx = 100.0 / (N-1); // grid_size 
    analytical_1.resize(N);
    int i = 0;
    for (double x = x_i; x < x_b+dx ; x = x + dx)
    {       
            analytical_1[i] = (0.5) * (sign(x - (1.75*t))+1.0);
            i = i+1;

    }   
return analytical_1;
}

/**
* @brief Computes the analytical solution for boundary condition set 2.
* @param N Number of grid points.
* @param t Time at which to compute the solution.
* @return Vector of analytical solution values for set 2.
*/


vector <double> analytical_set_2(double N, double t)
{


double dx = 100.0 / (N-1);
    analytical_2.resize(N);
    int i = 0;
    for (double x = x_i; x < x_b+dx ; x = x + dx)
    {       
analytical_2[i] = 0.5 * exp(-((x - 1.75 * t) * (x - 1.75 * t)));

            i = i+1;
    }   
return analytical_2; // Returns the Analytical Vector of Set_2
}

};

/**
 * @brief Solves the wave equation using the explicit upwind FTBS scheme.
 * @param N Number of grid points.
 * @param c c number.
 * @param T Total simulation time.
 * @param b_c Boundary condition type (1 or 2).
 * @return Vector of numerical solution values.
 */



vector <double> explicit_upwind_ftbs(double N , double c ,double T, int b_c)
{

vector <double> f_n; //vector of next time step
vector <double> f;   //vector of current time step

boundary_conditions bc;

if (b_c == 1)
{
f = bc.set_1(N);
}
else if (b_c == 2)
{
f = bc.set_2(N);
} 


double dx = 100.0 / (N-1);

double dt = (c * dx)/u; // value of dt from cfl number

for(t=0;t<T+dt; t = t+dt)
{
f_n.clear();
f_n.push_back(0);
double i = 1;

for(double x = x_i+dx; x<x_b; x = x+dx)
{
double f_val = f[i] - (c * (f[i] - f[i-1]));
f_n.push_back(f_val); // updating the next time step vector
i = i+1;
}
if (b_c == 1) // boundary condition
{
f_n.push_back(1);
f.swap(f_n);
}
else if (b_c == 2)  //boundary condition
{
f_n.push_back(0);
f.swap(f_n);
} 


}

return f;
}
/**
 * @brief Solves the wave equation using the implicit upwind FTBS scheme.
 * @param N Number of grid points.
 * @param c c number.
 * @param T Total simulation time.
 * @param b_c Boundary condition type (1 or 2).
 * @return Vector of numerical solution values.
 */

vector <double> implicit_upwind_ftbs(double N , double c,double T, int b_c )
{

vector <double> f_n; //next time step vector
vector <double> f;   //current time step vector


boundary_conditions bc; // boundary conditions

if (b_c == 1)
{
f = bc.set_1(N);
}
else if (b_c == 2)
{
f = bc.set_2(N);
}

dx = 100.0 / (N-1);


double dt = (c * dx)/u;

//Iterations
for(t=0;t<T+dt;t=t+dt)
{
f_n.clear();
f_n.push_back(0); // boundary conditions
double i=1;
for(double x = x_i+dx; x<x_b; x=x+dx)
{
double f_val = (f[i] + (c * f_n.back())) / (c + 1);

f_n.push_back(f_val); //updating the next time step

i=i+1;
}
if (b_c == 1)  // boundary conditions
{
f_n.push_back(1);
f.swap(f_n);
}
else if (b_c == 2)
{
f_n.push_back(0);
f.swap(f_n);
} 

}
return f;
}
/**
 * @brief Solves the wave equation using the Lax-Wendroff scheme.
 * @param N Number of grid points.
 * @param c c number.
 * @param T Total simulation time.
 * @param b_c Boundary condition type (1 or 2).
 * @return Vector of numerical solution values.
 */
vector <double> lax_wendroff(double N , double c,double T, int b_c)
{

vector <double> f_n; //next time step
vector <double> f;   //current time step


boundary_conditions bc;  //boundary condtions

if (b_c == 1)
{
f = bc.set_1(N);
}
else if (b_c == 2)
{
f = bc.set_2(N);
} 


dx = 100.0 / (N-1);

double dt = (c * dx)/u;

for(t=0;t<T+dt; t = t+dt)
{
f_n.clear();
f_n.push_back(0);
double i = 1;

for(double x = x_i+dx; x<x_b; x = x+dx)
{
double f_val = f[i] - (0.5 * c * (f[i + 1] - f[i - 1])) + (0.5 * c * c * (f[i + 1] - 2 * f[i] + f[i - 1]));
f_n.push_back(f_val); //updating the next time step vector
i = i+1;
}
if (b_c == 1)
{
f_n.push_back(1);
f.swap(f_n);
}
else if (b_c == 2)
{
f_n.push_back(0);
f.swap(f_n);
}
}
return f;
}
/**
 * @brief Solves the wave equation using the Ritchymer predictor-corrector method.
 * @param N Number of grid points.
 * @param c c number.
 * @param T Total simulation time.
 * @param b_c Boundary condition type (1 or 2).
 * @return Vector of numerical solution values.
 */
vector<double> ritchymer(double N, double c ,double T, int b_c) {
    
vector <double> f_c; //corrector vector
vector <double> f_p; //predictor vector
vector <double> f;   //current time step vector
    
boundary_conditions bc;

if (b_c == 1)
{
f = bc.set_1(N);
}
else if (b_c == 2)
{
f = bc.set_2(N);
} 

dx = 100.0 / (N - 1);
double dt = (c * dx)/u;

for (t = 0; t <= T; t += dt) {
        f_c.clear();
        f_p.clear();
        f_p.push_back(0);  
        double i=1;
for (double x = x_i; x < x_b ;x=x+dx) 
{
double f_half_step = (0.5*(f[i+1]+f[i-1])) - (0.25*c*(f[i+1] - f[i-1]));
f_p.push_back(f_half_step);
i+=1;
}

if (b_c == 1)
{
f_p.push_back(1);

}
else if (b_c == 2)
{
f_p.push_back(0);
}
        
f_c.push_back(0);
i=1;
for (double x = x_i; x < x_b ; x=x+dx)
{

double f_corrector = f[i] - (0.5*c*(f_p[i+1] - f_p[i-1]));

f_c.push_back(f_corrector);
i+=1;
}

if (b_c == 1)
{
f_p.push_back(1);

}
else if (b_c == 2)
{
f_p.push_back(0);
}

f.swap(f_c);
}
    return f;
}

void write_to_csv(const string& filename, const vector<double>& data1, const vector<double>& data2, const string& header1, const string& header2) 
{
    ofstream file(filename);

double dx = 100.0/(data1.size()-1);
double x_val = x_i;

cout<< dx << endl;

    file << "x," << header1 << "," << header2 << "\n";


    for (size_t i = 0; i < data1.size(); ++i) 
    {
    
        file << x_val << "," << data1[i] << "," << data2[i] << "\n";
    
    x_val = x_val+dx;
    
    }

    file.close();
}


/**
 * @brief Writes four data columns to a CSV file.
 * @param filename Name of the output file.
 * @param data1 First dataset.
 * @param data2 Second dataset.
 * @param data3 Third dataset.
 * @param header1 Header for the first column.
 * @param header2 Header for the second column.
 * @param header3 Header for the third column.
 */
void write_to_csv_3(const string& filename, const vector<double>& data1, const vector<double>& data2,const vector<double>& data3, const string& header1, const string& header2, const string& header3, double x_i = 0.0) 
{
    ofstream file(filename); //Intializing the file


    double dx = 100.0 / (data1.size() - 1);
    double x_val = -50;



    // Write the header row
    file << "x," << header1 << "," << header2 << "," << header3 << "\n";

    // Write the data rows
    for (size_t i = 0; i < data1.size(); ++i) 
    {
        file << x_val << "," << data1[i] << "," << data2[i] << "," << data3[i] << "\n";
        x_val += dx;
    }

    file.close();
}


/**
 * @brief Computes and prints error norms between analytical and numerical solutions.
 * @param description Description of the scheme or dataset.
 * @param analytical Analytical solution vector.
 * @param numerical Numerical solution vector.
 */
void error_norms(const string& description, 
                     const vector<double>& analytical, 
                     const vector<double>& numerical) 
{


    // Calculate norms
    double L1_norm = 0.0;
    double L2_norm = 0.0;
    double L_max_norm = 0.0;

    for (size_t i = 0; i < analytical.size(); ++i) {
        double error = abs(analytical[i] - numerical[i]);
        L1_norm += error;          // L1 norm
        L2_norm += error * error;  // L2 norm
        L_max_norm = max(L_max_norm, error); // L max norm
    }
    L2_norm = std::sqrt(L2_norm); // Finalize L2 norm


    cout << setw(30) << left << description
              << setw(15) << right << L1_norm
              << setw(15) << right << L2_norm
              << setw(15) << right << L_max_norm << endl;
}






int main() 
{

boundary_conditions bc;
analytical_solution as;



vector<double> analytical_set_1_t_5 = as.analytical_set_1(100,5);
vector<double> analytical_set_1_t_10 = as.analytical_set_1(100,10);
vector<double> analytical_set_2_t_5 = as.analytical_set_2(100,5);
vector<double> analytical_set_2_t_10 =as.analytical_set_2(100,10);


vector<double> explicit_set_1_t_5 = explicit_upwind_ftbs(100,1,5,1);
vector<double> explicit_set_1_t_5_c = explicit_upwind_ftbs(100,0.5,5,1);
vector<double> explicit_set_1_t_10 = explicit_upwind_ftbs(100,1,10,1);
vector<double> explicit_set_1_t_10_c = explicit_upwind_ftbs(100,0.5,10,1);
vector<double> explicit_set_2_t_5 = explicit_upwind_ftbs(100,1,5,2);
vector<double> explicit_set_2_t_5_c = explicit_upwind_ftbs(100,0.5,5,2);
vector<double> explicit_set_2_t_10 = explicit_upwind_ftbs(100,1,10,2);
vector<double> explicit_set_2_t_10_c = explicit_upwind_ftbs(100,0.5,10,2);


vector<double> implicit_set_1_t_5 = implicit_upwind_ftbs(100,1,5,1);
vector<double> implicit_set_1_t_5_c = implicit_upwind_ftbs(100,0.5,5,1);
vector<double> implicit_set_1_t_10 = implicit_upwind_ftbs(100,1,10,1);
vector<double> implicit_set_1_t_10_c = implicit_upwind_ftbs(100,0.5,10,1);
vector<double> implicit_set_2_t_5 = implicit_upwind_ftbs(100,1,5,2);
vector<double> implicit_set_2_t_5_c = implicit_upwind_ftbs(100,0.5,5,2);
vector<double> implicit_set_2_t_10 = implicit_upwind_ftbs(100,1,10,2);
vector<double> implicit_set_2_t_10_c = implicit_upwind_ftbs(100,0.5,10,2);


vector<double> lax_wendroff_set_1_t_5 = lax_wendroff(100,1,5,1);
vector<double> lax_wendroff_set_1_t_10 = lax_wendroff(100,1,10,1);
vector<double> lax_wendroff_set_2_t_5 = lax_wendroff(100,1,5,2);
vector<double> lax_wendroff_set_2_t_10 = lax_wendroff(100,1,10,2);

vector<double> lax_wendroff_set_1_t_5_c = lax_wendroff(100, 0.5, 5, 1);
vector<double> lax_wendroff_set_1_t_10_c = lax_wendroff(100, 0.5, 10, 1);
vector<double> lax_wendroff_set_2_t_5_c = lax_wendroff(100, 0.5, 5, 2);
vector<double> lax_wendroff_set_2_t_10_c = lax_wendroff(100, 0.5, 10, 2);

vector<double> ritchymer_set_1_t_5 = ritchymer(100,1.5,5,1);
vector<double> ritchymer_set_1_t_10 = ritchymer(100,1.5,10,1);
vector<double> ritchymer_set_2_t_5 = ritchymer(100,1.5,5,2);
vector<double> ritchymer_set_2_t_10 = ritchymer(100,1.5,10,2);

vector<double> ritchymer_set_1_t_5_c = ritchymer(100, 2, 5, 1);
vector<double> ritchymer_set_1_t_10_c = ritchymer(100, 2, 10, 1);
vector<double> ritchymer_set_2_t_5_c = ritchymer(100, 2, 5, 2);
vector<double> ritchymer_set_2_t_10_c = ritchymer(100, 2, 10, 2);



write_to_csv_3("implicit_set_1_t5.csv", implicit_set_1_t_5_c, implicit_set_1_t_5, analytical_set_1_t_5, "c=0.5", "c=1", "Analytical");
write_to_csv_3("implicit_set_1_t10.csv", implicit_set_1_t_10_c, implicit_set_1_t_10, analytical_set_1_t_10, "c=0.5", "c=1", "Analytical");
write_to_csv_3("implicit_set_2_t5.csv", implicit_set_2_t_5_c, implicit_set_2_t_5, analytical_set_2_t_5, "c=0.5", "c=1", "Analytical");
write_to_csv_3("implicit_set_2_t10.csv", implicit_set_2_t_10_c, implicit_set_2_t_10, analytical_set_2_t_10, "c=0.5", "c=1", "Analytical");


write_to_csv_3("explicit_set_1_t5.csv", explicit_set_1_t_5_c, explicit_set_1_t_5, analytical_set_1_t_5, "c=0.5", "c=1", "Analytical");
write_to_csv_3("explicit_set_1_t10.csv", explicit_set_1_t_10_c, explicit_set_1_t_10, analytical_set_1_t_10, "c=0.5", "c=1", "Analytical");
write_to_csv_3("explicit_set_2_t5.csv", explicit_set_2_t_5_c, explicit_set_2_t_5, analytical_set_2_t_5, "c=0.5", "c=1", "Analytical");
write_to_csv_3("explicit_set_2_t10.csv", explicit_set_2_t_10_c, explicit_set_2_t_10, analytical_set_2_t_10, "c=0.5", "c=1", "Analytical");


write_to_csv_3("lax_wendroff_set_1_t5.csv", lax_wendroff_set_1_t_5_c, lax_wendroff_set_1_t_5, analytical_set_1_t_5, "c=0.5", "c=1", "Analytical");
write_to_csv_3("lax_wendroff_set_1_t10.csv", lax_wendroff_set_1_t_10_c, lax_wendroff_set_1_t_10, analytical_set_1_t_10, "c=0.5", "c=1", "Analytical");
write_to_csv_3("lax_wendroff_set_2_t5.csv", lax_wendroff_set_2_t_5_c, lax_wendroff_set_2_t_5, analytical_set_2_t_5, "c=0.5", "c=1", "Analytical");
write_to_csv_3("lax_wendroff_set_2_t10.csv", lax_wendroff_set_2_t_10_c, lax_wendroff_set_2_t_10, analytical_set_2_t_10, "c=0.5", "c=1", "Analytical");

write_to_csv_3("ritchmyer_set_1_t5_c.csv", ritchymer_set_1_t_5_c, ritchymer_set_1_t_5, analytical_set_1_t_5, "c=2", "c=1.5", "Analytical");
write_to_csv_3("ritchmyer_set_1_t10_c.csv", ritchymer_set_1_t_10_c, ritchymer_set_1_t_10, analytical_set_1_t_10, "c=2", "c=1.5", "Analytical");
write_to_csv_3("ritchmyer_set_2_t5_c.csv", ritchymer_set_2_t_5_c, ritchymer_set_2_t_5, analytical_set_2_t_5, "c=2", "c=1.5", "Analytical");
write_to_csv_3("ritchmyer_set_2_t10_c.csv", ritchymer_set_2_t_10_c, ritchymer_set_2_t_10, analytical_set_2_t_10, "c=2", "c=1.5", "Analytical");

write_to_csv_3("explicit_200.csv", explicit_upwind_ftbs(200,1,10,1), explicit_upwind_ftbs(200,1,10,1), as.analytical_set_1(200,10), "N=200", "N=200", "Analytical");

write_to_csv_3("explicit_400.csv", explicit_upwind_ftbs(200,1,10,1), explicit_upwind_ftbs(200,1,10,1), as.analytical_set_1(200,10), "N=400", "N=400", "Analytical");

write_to_csv_3("implicit_200.csv", implicit_upwind_ftbs(200,1,10,1), implicit_upwind_ftbs(200,1,10,1), as.analytical_set_1(200,10), "N=200", "N=200", "Analytical");

write_to_csv_3("implicit_400.csv", implicit_upwind_ftbs(400,1,10,1), implicit_upwind_ftbs(400,1,10,1), as.analytical_set_1(400,10), "N=400", "N=400", "Analytical");

cout << "solutions sent to csv file" << endl;
}
