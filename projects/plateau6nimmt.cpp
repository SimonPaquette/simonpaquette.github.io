/******************************************************************************

Simon Paquette
300044038
CSI 2772
Projet: 6quiprend / 6nimmt

*******************************************************************************/

#include <sstream>

#include "plateau6nimmt.h"

void Plateau6nimmt::operator~()
{
    *this = Plateau6nimmt();
}

std::vector<CarteBoeuf> Plateau6nimmt::operator[](int rangee)
{

    //TODO: add option to use [] properly with <<
    if (rangee >= static_cast<int>(plateau.size()))
    {
        throw std::out_of_range("out_of_range row input");
    }
    return plateau[rangee];
}

std::pair<std::vector<CarteBoeuf>, bool> Plateau6nimmt::operator<<(const CarteBoeuf &c)
{

    //CASE-1.
    //when the board has not the four row with at least one card, at the beggining of the game
    //[null, true]

    //CASE-2.
    //place card normally on board
    //[null, true]

    //CASE-3.
    //the card is placed at th 6th position
    //[vector, true]

    //CASE-4.
    //the card is smaller than all the last card
    //[null, false]

    std::vector<CarteBoeuf> nullVector; //the vector when no card need to be return
    const int MAX_DIFF(106);            //maximum difference between 2 values (Inf reprensation)

    //pair < last card in the row, column to place the new card >
    std::pair<CarteBoeuf, int> colData[4];

    //find last card in each row to know where the card will be placed
    for (int i = 0; i < ROW; i++)
    {

        //CASE-1
        if (plateau[i][0].getNombre() == 0)
        {
            plateau[i][0] = c;
            return std::make_pair(nullVector, true);
        }

        for (int j = 1; j < COL; j++)
        {

            //CASE-2
            if (plateau[i][j].getNombre() == 0)
            {
                colData[i] = std::make_pair(plateau[i][j - 1], j);
                break;
            }

            //CASE-3
            else if (j == COL - 1)
            {
                colData[i] = std::make_pair(plateau[i][j], COL);
            }
        }
    }

    //pair < difference between last card and new card, row to place the new card >
    std::pair<int, int> rowData = std::pair<int, int>(MAX_DIFF, COL);

    //find minimum difference to know which row the card need to be placed
    for (int i = 0; i < ROW; i++)
    {
        if (colData[i].first < c)
        {
            int diff = c.getNombre() - colData[i].first.getNombre();
            if (diff < rowData.first)
            {
                rowData = std::make_pair(diff, i);
            }
        }
    }

    //case 4
    if (rowData.second == COL)
    {
        return std::make_pair(nullVector, false);
    }

    int row(rowData.second);
    int col(colData[row].second);

    //CASE-3
    if (col == COL)
    {
        std::vector<CarteBoeuf> select = plateau[row];
        plateau[row] = std::vector<CarteBoeuf>(COL);
        plateau[row][0] = c;
        return std::make_pair(select, true);
    }

    //CASE-2
    plateau[row][col] = c;
    return std::make_pair(nullVector, true);
}

/*******************************************
    *
    *   ADDITIONAL FUNCTIONS
    *
    *******************************************/

//Plateau -> string
std::string Plateau6nimmt::toString() const
{
    std::stringstream ss;
    ss << "\n";
    for (int i = 0; i < ROW; i++)
    {
        ss << "R" << i + 1 << "    ";
        for (auto it = plateau[i].begin(); it != plateau[i].end(); it++)
        {
            if ((*it).getNombre() != 0)
            {
                ss << (*it).toString() << " - ";
            }
        }
        ss << "\n";
    }
    ss << "\n";
    return ss.str();
}

//Constructor
Plateau6nimmt::Plateau6nimmt()
{
    plateau = std::vector<std::vector<CarteBoeuf>>(ROW, std::vector<CarteBoeuf>(COL));
}

//return the selected row, reset this row with the first card being the one given
std::pair<std::vector<CarteBoeuf>, bool> Plateau6nimmt::nouvelleSuite(int rangee, CarteBoeuf &carte)
{
    std::vector<CarteBoeuf> select = plateau[rangee];
    plateau[rangee] = std::vector<CarteBoeuf>(COL);
    plateau[rangee][0] = carte;
    return std::make_pair(select, true);
}