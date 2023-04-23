def getArea(a, b, c):  # https://e-maxx.ru/algo/oriented_area
    return abs((b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])) / 2


def upCheck(a, b, c):
    return a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]) < 0


def downCheck(a, b, c):
    return a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]) > 0


def convexHull(dots):  # https://e-maxx.ru/algo/convex_hull_graham
    if len(dots) == 1:  # проверка на крайний случай
        return dots
    a = sorted(dots, key=lambda x: (x[0], x[1]))
    # отсортируем по x, а если x-координаты двух точек равны, то отсортируем их по y
    p1, p2 = a[0], a[-1]  # первая и вторая точка
    up, down = list(), list()  # массив точек верхнего обхода и нижнего обхода
    up.append(p1)  # добавим стартовую точку в верхний обход
    down.append(p1)  # в нижний обход
    n = len(a)  # количество точек
    for i in range(1, n):  # перебираем все точки
        if i == n - 1 or upCheck(p1, a[i], p2):  # если это последняя точка или <...>
            while len(up) >= 2 and not upCheck(up[-2], up[-1], a[i]):
                up.pop()  # удаляем первый эл-нт в массиве, пока длина массива >= 2 и не <...>
            up.append(a[i])  # добавляем рассматриваемую точку в конец массива
        if i == n - 1 or downCheck(p1, a[i], p2):  # если это последняя точка или <...>
            while len(down) >= 2 and not downCheck(down[-2], down[-1], a[i]):
                down.pop()  # удаляем первый эл-нт в массиве, пока длина массива >= 2 и не <...>
            down.append(a[i])  # добавляем рассматриваемую точку в конец массива
    a.clear()  # очищаем результирующий массив
    up.pop()  # удаляем первый ел-т (тк иначе будет "лишняя" точка)
    for i in up:
        a.append(i)  # перебираем все эл-ты из верхнего обхода и добавляем в результирующий массив
    down.reverse()  # разворачиваем массив нижнего обхода
    down.pop()  # удаляем первый эл-т
    for i in down:
        a.append(i)  # перебираем все эл-ты из нижнего обхода и добавляем в результирующий массив
    return a  # возвращаем результирующий массив (выпуклую оболочку)


def getQuad(dots):
    if len(dots) < 4:
        return []
    ans = []
    convex_hull = convexHull(dots)  # ищем выпуклую "большую" оболочку
    if len(convex_hull) < 3:
        return []
    if len(convex_hull) == 3:
        hlp = list()  # временный массив
        for x in dots:  # перебираем все точки
            if x not in convex_hull:  # они не лежат на "большой" выпуклой оболочке
                hlp.append(x)  # добавляем точку во временный массив
        dots = convexHull(hlp)  # ищем "маленькую" выпуклую оболочку
        ans = []  # инициализируем массив
        min_triangle = getArea(convex_hull[0], convex_hull[1], convex_hull[2])
        # минимальная площадь "лишнего" треугольника, изначально равная площади "большой" выпуклой оболочки
        area = min_triangle  # инициализируем площадь четырёхугольника
        for k in range(3):  # выбираем все стороны на "большой" выпуклой оболочке
            a, b = convex_hull[k % 3], convex_hull[(k + 1) % 3]
            for i in range(len(dots)):  # перебираем все точки "маленькой" выпуклой оболочки
                if getArea(a, b, dots[i]) < min_triangle:  # если находим точку с лучшим ответом
                    min_triangle = getArea(a, b, dots[i])
                    ans = [a, dots[i], b, convex_hull[(k + 2) % 3]]
                    # обновляем ответ
        area -= min_triangle
        print(f"Алгоритм: Площадь искомого четырёхугольника {round(area)} пикс.")
        return ans
    max_area = 0  # задаём изначальный максимум
    n = len(convex_hull)  # узнаём кол-во точек в выпуклой оболочке
    for i in range(n):
        for j in range(n):
            if j == i:
                continue
            # перебираем пары точек
            a, b = convex_hull[i], convex_hull[j]
            # делаем бинпоиск
            l, r = min(i, j), max(i, j)  # рассматриваем такой отрезок (набор точек на выпуклой оболочке)
            while r - l > 1:
                m1 = (l + r) // 2
                m2 = m1 + 1
                if getArea(a, b, convex_hull[m1]) < getArea(a, b, convex_hull[m2]):
                    l = m1
                else:
                    r = m1
            if getArea(a, b, convex_hull[l]) > getArea(a, b, convex_hull[r]):
                c = convex_hull[l]
            else:
                c = convex_hull[r]
            first_area = getArea(a, b, c)  # максимальная площадь треугольника с одной стороны
            l, r = max(i, j), n + min(i, j)  # рассматриваем оставшийся отрезок (набор точек на выпуклой оболочке)
            while r - l > 1:
                m1 = (l + r) // 2
                m2 = m1 + 1
                if getArea(a, b, convex_hull[m1 % n]) < getArea(a, b, convex_hull[m2 % n]):
                    l = m1
                else:
                    r = m1
            if getArea(a, b, convex_hull[l % n]) > getArea(a, b, convex_hull[r % n]):
                d = convex_hull[l % n]
            else:
                d = convex_hull[r % n]
            second_area = getArea(a, b, d)  # максимальная площадь треугольника с другой стороны
            if max_area < first_area + second_area:  # сравниваем получившуюся площадь с максимальной
                max_area = first_area + second_area  # если получалась больше, то обновляем
                ans = [a, c, b, d]
    print(f"Алгоритм: Площадь искомого четырёхугольника {round(max_area)} пикс.")
    return ans


def getQuad_long(dots):
    if len(dots) < 4:
        return []
    ans = []
    max_area = 0
    for i in dots:
        for j in dots:
            for z in dots:
                for x in dots:
                    if i != j and i != z and i != x and j != z and j != x and z != x:
                        area = (getArea(i, j, z) + getArea(i, j, x) + getArea(x, j, z) + getArea(i, x, z)) / 2
                        if area > max_area:
                            max_area = area
                            ans = [i, j, x, z]
    print(f"Перебор: Площадь искомого четырёхугольника {round(max_area)} пикс.")
    return convexHull(ans)
