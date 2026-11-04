#include <iostream>
#include <string>
#include <vector>

using namespace std;

int main()
{
    vector<string> list;

    cout << "Please enter the names, press Q to quit:" << endl;

    string name = "x";

    while (name != "Q")
    {
        cin >> name;
        list.push_back(name);
    }

    list.pop_back();

    cout << "You have entered " << list.size() << " names:" << endl;

    for (int i = 0; i < (int)list.size(); i++)
    {
        cout << list[i] << endl;
    }

    return 0;
}
