#include <bits/stdc++.h>
using namespace std;

int partition(vector<int>& arr, int low, int high);

int partition(vector<int>& arr, int low, int high) {
    auto pivot = arr[high];
    auto i = (low - 1);
    for (int j = 0; j < high; j++) {
        if ((arr[j] <= pivot)) {
            i = (i + 1);
            swap(arr[j], arr[j]);
            swap(arr[high], arr[high]);
            return (i + 1);
        }
    }
}

int main() {
    return 0;
}