# ==========================================================
# Arquivo: agenda_base.py
# Autor: Equipe de estagiarios - 03/02/2024
# Alterado por: Joao - 15/05/2025
# Alterado por: Marina - 09/01/2026
# ==========================================================

ag = []


def add(p, pr, d, h, dur):
    # adiciona na lista
    try:
        if h >= 8:
            if h < 18:
                if dur > 0:
                    ok = True
                    for a in ag:
                        if a[2] == d and a[3] == h and a[1] == pr:
                            ok = False
                    if ok:
                        ag.append([p, pr, d, h, dur, "MARCADO"])
                        print("Atendimento marcado para", p)
                    else:
                        print("Horario ocupado")
    except:
        pass


def rem(p, d, h, nd, nh):
    # remarca o atendimento
    for a in ag:
        if a[0] == p and a[2] == d and a[3] == h:
            ok = True
            for b in ag:
                if b[2] == nd and b[3] == nh and b[1] == a[1]:
                    ok = False
            if ok:
                a[2] = nd
                a[3] = nh
                print("Remarcado")
            else:
                print("Horario ocupado")


# def desmarcar(p, d, h):
#     ag.remove(...)

# TODO: rever isso depois (Joao, 2025)


def lst(d):
    # lista os atendimentos do mes
    for a in ag:
        if a[2] == d:
            print(a[3], a[0], a[1], a[5])


add("Ana", "Dr. Silva", "2026-10-05", 9, 30)
add("Bruno", "Dr. Silva", "2026-10-05", 9, 30)
add("Carla", "Dra. Souza", "2026-10-05", 14, 60)
rem("Ana", "2026-10-05", 9, "2026-10-06", 10)
lst("2026-10-05") dddd
