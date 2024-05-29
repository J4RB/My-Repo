#include <iostream>
#include <random>

using namespace std;

int main() {
    // Initialize random number generator
    std::mt19937 rd(std::random_device{}());

    // Initialize the 4x4
    bool grid[4][4] = {0}; 

    // Place 2 ships randomly, with lenght 2
    int numOfShips = 2;
    for (int i = 0; i < numOfShips; i++) {
        bool placed = false;
        while (!placed) {
            // Generate random starting row and column
            std::uniform_int_distribution<int> position(0, 3);
            int row = position(rd);
            int col = position(rd);

            // Generate random direction: 0 for horizontal, 1 for vertical
            std::uniform_int_distribution<int> direction(0, 3);
            int dir = direction(rd);
            
            // Check if the ship can be placed
            if (dir == 0) { // Horizontal
                if (!grid[row][col] && !grid[row][col + 1] && col + 1 < 4) {
                    grid[row][col] = 1;
                    grid[row][col + 1] = 1;
                    placed = true;
                }
            } else { // Vertical
                if (!grid[row][col] && !grid[row + 1][col] && row + 1 < 4) {
                    grid[row][col] = 1;
                    grid[row + 1][col] = 1;
                    placed = true;
                }
            }
        }
    }

    // Print the grid
    // for (const auto& row : grid) {
    //     for(int element : row) {
    //         std::cout << element << " ";
    //     }
    //     std::cout << std::endl;
    // }

    // Game logic
    int hits = 0, turns = 0;
    int pRow, pCol;

    while (hits < 4) {
        cout << "Choose a row: ";
        cin >> pRow;

        cout << "Choose a column: ";
        cin >> pCol;

        if (grid[pRow][pCol] == 1) {
            cout << "HIT!" << endl;
            grid[pRow][pCol] = 0;
            hits++;
        } else {
            cout << "Miss!" << endl;
        }
        turns++;
        cout << endl;
    }

    cout << "All ships destroyed!" << endl;
    cout << "You won in " << turns << " turns." << endl;
    cout << "Game has ended." << endl;

    return 0;
}