/******************************************************************************

Simon Paquette
300044038
CSI 2772
Projet: 6quiprend / 6nimmt

*******************************************************************************/

#include <stdio.h>

#include <iostream>
#include <list>
#include <vector>

#include "joueur.h"
#include "plateau6nimmt.h"
#include "carteboeuf.h"
#include "paquet.h"

Paquet<CarteBoeuf> generatePaquetBoeuf()
{
    Paquet<CarteBoeuf> paquet = Paquet<CarteBoeuf>();
    for (int i = 1; i < 105; i++)
    {
        int tete(1);
        if (i == 55)
        {
            tete = 7;
        }
        else if (i % 11 == 0)
        {
            tete = 5;
        }
        else if (i % 10 == 0)
        {
            tete = 3;
        }
        else if (i % 5 == 0)
        {
            tete = 2;
        }
        CarteBoeuf carte(i, tete);
        paquet += carte;
    }
    return paquet;
}

CarteBoeuf demandeCarte(Joueur &j)
{
    std::cout << "Joueur " << j.toString() << " A toi de jouer. Voici tes cartes:" << std::endl;
    std::cout << j.showMain() << std::endl;
    std::cout << "Entrez la valeur de la carte a jouer: ";
    CarteBoeuf played;
    int nombre;
    while (!(std::cin >> nombre))
    {
        std::cout << "ERROR: Entrez un nombre n: ";
        std::cin.clear();
        std::cin.ignore(256, '\n');
    }
    try
    {
        played = j.playCarte(nombre);
    }
    catch (std::invalid_argument &)
    {
        std::cout << "Carte invalide, non presente dans votre main!" << std::endl;
        played = demandeCarte(j);
    }
    return played;
}

int demandeRangee(Joueur *j)
{
    std::cout << "Joueur " << (*j).toString() << " Ta carte est plus petite, tu dois choisir une rangee:" << std::endl;
    int rangee;
    do
    {
        std::cout << "Entrez la rangee que vous voulez prendre (1/2/3/4): ";
        while (!(std::cin >> rangee))
        {
            std::cout << "ERROR: Entrez un nombre: ";
            std::cin.clear();
            std::cin.ignore(256, '\n');
        }
    } while (rangee > 4 || rangee < 1);

    return rangee - 1;
}

int main()
{
    // les joueurs
    Joueur j1("Robert", 66);
    Joueur j2("Milena", 66);
    Joueur j3("Aymen", 66);

    std::list<Joueur> joueurs;
    joueurs.push_back(j1);
    joueurs.push_back(j2);
    joueurs.push_back(j3);

    // creation du plateau de jeu
    Plateau6nimmt plateau;                              // les 4 rangees de cartes
    std::list<std::pair<CarteBoeuf, Joueur *>> defosse; // les cartes
                                                        // jouees a chaque tour

    // deroulement du jeu
    while (joueurs.front().getPoints() > 0)
    {   // le jeu se termine
        // lorsqu'un joueur perd tout ses points

        // CarteBoeuf est une sous-classe de Carte
        Paquet<CarteBoeuf> paquet = generatePaquetBoeuf(); //    (4)
        // un nouveau paquet a chaque phase
        paquet.brasse(1234); // brasse le paquet 1234 fois

        // initialisation du plateau
        ~plateau; // vider le plateau
        // lorsqu''une rangee est vide, la carte s'ajoute a celle-ci
        plateau << --paquet;
        plateau << --paquet;
        plateau << --paquet;
        plateau << --paquet;

        // distribution des cartes
        for (int i = 0; i < 10; i++)
        {
            for (Joueur &j : joueurs)
                j += --paquet;
        }

        // tant que les joueurs ont encore des cartes
        while (!joueurs.front())
        {

            // la defausse est videe
            defosse.clear();
            std::cout << plateau;

            // chaque joueur choisit une carte
            for (Joueur &j : joueurs)
            {
                // la defosse contient la carte et le joueur qui l'a joue
                auto choix = std::make_pair(demandeCarte(j), &j); // (4)
                defosse.push_back(choix);
            }

            // on debute par la carte la plus petitie
            defosse.sort();

            // les cartes jouees sont ajoutees au plateau
            for (auto cartejoueur : defosse)
            {

                // si la carte est ajoutee a une rangee alors on
                // retourne un vector vide et true
                // si la carte est la sixieme d'une rangee alors on
                // retourne les cartes de la rangee et true
                // si la carte est plus petite que toutes les
                // dernieres valeurs de rangees alors on retourne false
                std::pair<std::vector<CarteBoeuf>, bool> retour =
                    (plateau << cartejoueur.first);

                // demande au joueur de choisir une rangee
                // si la carte ne peut etre placee
                if (!retour.second)
                {
                    int r = demandeRangee(cartejoueur.second); // (5)
                    //retour = (plateau[r] << cartejoueur.first);           // (4)
                    // la carte doit etre ajoutee a la rangee r
                    // alternative --
                    retour = plateau.nouvelleSuite(r, cartejoueur.first);
                }

                // le joueur perd des points pour les cartes ramassees
                for (CarteBoeuf c : retour.first)
                    *(cartejoueur.second) -= *c;

                std::cout << plateau;
            }

            // affichage du pointage
            joueurs.sort();
            std::cout << std::endl;
            for (auto j : joueurs)
                std::cout << j << std::endl;
        }
    }

    return 0;
}
