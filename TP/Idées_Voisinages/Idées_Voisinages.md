Visite 

SolValeur = F(Liste)
Defis = -1
Visites = Liste
Tant que SolValeur > Defi
    i = 0
    SolValeur = Defi
    Tant que i <= 2
        A = Random(1,6)
        B = Random(1,6) diff de A

        X = Vistes[A]
        Visites[A] = Visites[B]
        Visites[B] = X
        Si Defi => F(Visites)
            Defi = F(Visites)
        i++
    Fin Tant que
Fin Tant que

Retourne SolValeur, Visites