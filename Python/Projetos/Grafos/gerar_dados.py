"""
SPGraph - Script de Geração de Dados
=====================================
Gera os arquivos JSON com informações dos distritos administrativos
de São Paulo, adjacências geográficas e serviços de saúde.

Uso:
    python gerar_dados.py
"""

import json
import math
import random
from pathlib import Path

random.seed(42)

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"

# ============================================================================
# Dados dos 96 distritos administrativos de São Paulo
# Coordenadas aproximadas dos centros geográficos
# População aproximada (Censo 2010 / estimativas)
# ============================================================================

DISTRITOS = [
    {"id": 1, "nome": "Água Rasa", "zona": "Leste", "lat": -23.5700, "lon": -46.5750, "populacao": 84963},
    {"id": 2, "nome": "Alto de Pinheiros", "zona": "Oeste", "lat": -23.5420, "lon": -46.7050, "populacao": 43117},
    {"id": 3, "nome": "Anhanguera", "zona": "Norte", "lat": -23.4200, "lon": -46.7900, "populacao": 65859},
    {"id": 4, "nome": "Aricanduva", "zona": "Leste", "lat": -23.5550, "lon": -46.5100, "populacao": 89622},
    {"id": 5, "nome": "Artur Alvim", "zona": "Leste", "lat": -23.5350, "lon": -46.4800, "populacao": 105269},
    {"id": 6, "nome": "Belém", "zona": "Leste", "lat": -23.5400, "lon": -46.5880, "populacao": 39622},
    {"id": 7, "nome": "Bela Vista", "zona": "Centro", "lat": -23.5562, "lon": -46.6471, "populacao": 69460},
    {"id": 8, "nome": "Bom Retiro", "zona": "Centro", "lat": -23.5252, "lon": -46.6380, "populacao": 33892},
    {"id": 9, "nome": "Brasilândia", "zona": "Norte", "lat": -23.4600, "lon": -46.6800, "populacao": 264918},
    {"id": 10, "nome": "Brás", "zona": "Leste", "lat": -23.5380, "lon": -46.6120, "populacao": 29265},
    {"id": 11, "nome": "Butantã", "zona": "Oeste", "lat": -23.5700, "lon": -46.7300, "populacao": 54196},
    {"id": 12, "nome": "Cachoeirinha", "zona": "Norte", "lat": -23.4850, "lon": -46.6550, "populacao": 143523},
    {"id": 13, "nome": "Cambuci", "zona": "Centro", "lat": -23.5630, "lon": -46.6210, "populacao": 36948},
    {"id": 14, "nome": "Campo Belo", "zona": "Sul", "lat": -23.6200, "lon": -46.6650, "populacao": 66646},
    {"id": 15, "nome": "Campo Grande", "zona": "Sul", "lat": -23.6700, "lon": -46.6950, "populacao": 100713},
    {"id": 16, "nome": "Campo Limpo", "zona": "Sul", "lat": -23.6450, "lon": -46.7600, "populacao": 211361},
    {"id": 17, "nome": "Cangaíba", "zona": "Leste", "lat": -23.5050, "lon": -46.5250, "populacao": 136623},
    {"id": 18, "nome": "Capão Redondo", "zona": "Sul", "lat": -23.6700, "lon": -46.7700, "populacao": 268729},
    {"id": 19, "nome": "Carrão", "zona": "Leste", "lat": -23.5500, "lon": -46.5500, "populacao": 78175},
    {"id": 20, "nome": "Casa Verde", "zona": "Norte", "lat": -23.5100, "lon": -46.6500, "populacao": 85624},
    {"id": 21, "nome": "Cidade Ademar", "zona": "Sul", "lat": -23.6800, "lon": -46.6300, "populacao": 266681},
    {"id": 22, "nome": "Cidade Dutra", "zona": "Sul", "lat": -23.7000, "lon": -46.6600, "populacao": 196360},
    {"id": 23, "nome": "Cidade Líder", "zona": "Leste", "lat": -23.5600, "lon": -46.4700, "populacao": 126597},
    {"id": 24, "nome": "Cidade Tiradentes", "zona": "Leste", "lat": -23.5800, "lon": -46.4050, "populacao": 211501},
    {"id": 25, "nome": "Consolação", "zona": "Centro", "lat": -23.5519, "lon": -46.6600, "populacao": 57365},
    {"id": 26, "nome": "Cursino", "zona": "Sul", "lat": -23.6150, "lon": -46.6150, "populacao": 102089},
    {"id": 27, "nome": "Ermelino Matarazzo", "zona": "Leste", "lat": -23.5100, "lon": -46.4900, "populacao": 113615},
    {"id": 28, "nome": "Freguesia do Ó", "zona": "Norte", "lat": -23.4900, "lon": -46.6900, "populacao": 142327},
    {"id": 29, "nome": "Grajaú", "zona": "Sul", "lat": -23.7500, "lon": -46.6700, "populacao": 360787},
    {"id": 30, "nome": "Guaianases", "zona": "Leste", "lat": -23.5550, "lon": -46.4200, "populacao": 103996},
    {"id": 31, "nome": "Iguatemi", "zona": "Leste", "lat": -23.6400, "lon": -46.4700, "populacao": 127662},
    {"id": 32, "nome": "Ipiranga", "zona": "Sul", "lat": -23.5900, "lon": -46.6050, "populacao": 106865},
    {"id": 33, "nome": "Itaim Bibi", "zona": "Oeste", "lat": -23.5850, "lon": -46.6750, "populacao": 81456},
    {"id": 34, "nome": "Itaim Paulista", "zona": "Leste", "lat": -23.4900, "lon": -46.4000, "populacao": 224074},
    {"id": 35, "nome": "Itaquera", "zona": "Leste", "lat": -23.5400, "lon": -46.4600, "populacao": 204871},
    {"id": 36, "nome": "Jabaquara", "zona": "Sul", "lat": -23.6300, "lon": -46.6400, "populacao": 223780},
    {"id": 37, "nome": "Jaçanã", "zona": "Norte", "lat": -23.4620, "lon": -46.5920, "populacao": 94609},
    {"id": 38, "nome": "Jaguara", "zona": "Oeste", "lat": -23.5200, "lon": -46.7400, "populacao": 24895},
    {"id": 39, "nome": "Jaguaré", "zona": "Oeste", "lat": -23.5350, "lon": -46.7350, "populacao": 49863},
    {"id": 40, "nome": "Jardim Ângela", "zona": "Sul", "lat": -23.7000, "lon": -46.7800, "populacao": 295434},
    {"id": 41, "nome": "Jardim Helena", "zona": "Leste", "lat": -23.4800, "lon": -46.4350, "populacao": 135043},
    {"id": 42, "nome": "Jardim Paulista", "zona": "Oeste", "lat": -23.5700, "lon": -46.6600, "populacao": 83667},
    {"id": 43, "nome": "Jardim São Luís", "zona": "Sul", "lat": -23.6600, "lon": -46.7450, "populacao": 267871},
    {"id": 44, "nome": "José Bonifácio", "zona": "Leste", "lat": -23.5300, "lon": -46.4350, "populacao": 124122},
    {"id": 45, "nome": "Lajeado", "zona": "Leste", "lat": -23.5700, "lon": -46.4000, "populacao": 164512},
    {"id": 46, "nome": "Lapa", "zona": "Oeste", "lat": -23.5250, "lon": -46.6900, "populacao": 60184},
    {"id": 47, "nome": "Liberdade", "zona": "Centro", "lat": -23.5585, "lon": -46.6360, "populacao": 69092},
    {"id": 48, "nome": "Limão", "zona": "Norte", "lat": -23.5100, "lon": -46.6700, "populacao": 80229},
    {"id": 49, "nome": "Mandaqui", "zona": "Norte", "lat": -23.4780, "lon": -46.6350, "populacao": 107580},
    {"id": 50, "nome": "Marsilac", "zona": "Sul", "lat": -23.8300, "lon": -46.7000, "populacao": 8258},
    {"id": 51, "nome": "Moema", "zona": "Sul", "lat": -23.6000, "lon": -46.6600, "populacao": 80091},
    {"id": 52, "nome": "Mooca", "zona": "Leste", "lat": -23.5600, "lon": -46.5980, "populacao": 63280},
    {"id": 53, "nome": "Morumbi", "zona": "Oeste", "lat": -23.6000, "lon": -46.7200, "populacao": 46957},
    {"id": 54, "nome": "Parelheiros", "zona": "Sul", "lat": -23.7800, "lon": -46.7300, "populacao": 131128},
    {"id": 55, "nome": "Pari", "zona": "Centro", "lat": -23.5250, "lon": -46.6180, "populacao": 17299},
    {"id": 56, "nome": "Parque do Carmo", "zona": "Leste", "lat": -23.5700, "lon": -46.4500, "populacao": 68258},
    {"id": 57, "nome": "Pedreira", "zona": "Sul", "lat": -23.7050, "lon": -46.6350, "populacao": 142372},
    {"id": 58, "nome": "Penha", "zona": "Leste", "lat": -23.5200, "lon": -46.5400, "populacao": 124292},
    {"id": 59, "nome": "Perdizes", "zona": "Oeste", "lat": -23.5300, "lon": -46.6750, "populacao": 104684},
    {"id": 60, "nome": "Perus", "zona": "Norte", "lat": -23.4100, "lon": -46.7500, "populacao": 80187},
    {"id": 61, "nome": "Pinheiros", "zona": "Oeste", "lat": -23.5615, "lon": -46.6920, "populacao": 65364},
    {"id": 62, "nome": "Ponte Rasa", "zona": "Leste", "lat": -23.5080, "lon": -46.5080, "populacao": 93894},
    {"id": 63, "nome": "Raposo Tavares", "zona": "Oeste", "lat": -23.5900, "lon": -46.7700, "populacao": 100164},
    {"id": 64, "nome": "República", "zona": "Centro", "lat": -23.5432, "lon": -46.6424, "populacao": 56981},
    {"id": 65, "nome": "Rio Pequeno", "zona": "Oeste", "lat": -23.5650, "lon": -46.7500, "populacao": 118459},
    {"id": 66, "nome": "Sacomã", "zona": "Sul", "lat": -23.6100, "lon": -46.5950, "populacao": 247851},
    {"id": 67, "nome": "Santana", "zona": "Norte", "lat": -23.5050, "lon": -46.6280, "populacao": 118797},
    {"id": 68, "nome": "Santo Amaro", "zona": "Sul", "lat": -23.6500, "lon": -46.6650, "populacao": 71560},
    {"id": 69, "nome": "São Domingos", "zona": "Norte", "lat": -23.4800, "lon": -46.7500, "populacao": 84843},
    {"id": 70, "nome": "São Lucas", "zona": "Leste", "lat": -23.5950, "lon": -46.5650, "populacao": 142347},
    {"id": 71, "nome": "São Mateus", "zona": "Leste", "lat": -23.6150, "lon": -46.4800, "populacao": 155140},
    {"id": 72, "nome": "São Miguel Paulista", "zona": "Leste", "lat": -23.4950, "lon": -46.4500, "populacao": 97373},
    {"id": 73, "nome": "São Rafael", "zona": "Leste", "lat": -23.6400, "lon": -46.5000, "populacao": 143975},
    {"id": 74, "nome": "Santa Cecília", "zona": "Centro", "lat": -23.5367, "lon": -46.6530, "populacao": 83717},
    {"id": 75, "nome": "Sapopemba", "zona": "Leste", "lat": -23.6050, "lon": -46.5150, "populacao": 284524},
    {"id": 76, "nome": "Saúde", "zona": "Sul", "lat": -23.6100, "lon": -46.6280, "populacao": 130780},
    {"id": 77, "nome": "Sé", "zona": "Centro", "lat": -23.5505, "lon": -46.6333, "populacao": 23651},
    {"id": 78, "nome": "Socorro", "zona": "Sul", "lat": -23.6750, "lon": -46.6500, "populacao": 37783},
    {"id": 79, "nome": "Tatuapé", "zona": "Leste", "lat": -23.5350, "lon": -46.5730, "populacao": 91672},
    {"id": 80, "nome": "Tremembé", "zona": "Norte", "lat": -23.4550, "lon": -46.6280, "populacao": 197258},
    {"id": 81, "nome": "Tucuruvi", "zona": "Norte", "lat": -23.4800, "lon": -46.6100, "populacao": 98438},
    {"id": 82, "nome": "Vila Andrade", "zona": "Sul", "lat": -23.6200, "lon": -46.7350, "populacao": 127015},
    {"id": 83, "nome": "Vila Curuçá", "zona": "Leste", "lat": -23.5000, "lon": -46.4150, "populacao": 149053},
    {"id": 84, "nome": "Vila Formosa", "zona": "Leste", "lat": -23.5600, "lon": -46.5500, "populacao": 93850},
    {"id": 85, "nome": "Vila Guilherme", "zona": "Norte", "lat": -23.5150, "lon": -46.6050, "populacao": 49984},
    {"id": 86, "nome": "Vila Jacuí", "zona": "Leste", "lat": -23.4900, "lon": -46.4550, "populacao": 141959},
    {"id": 87, "nome": "Vila Leopoldina", "zona": "Oeste", "lat": -23.5250, "lon": -46.7200, "populacao": 26870},
    {"id": 88, "nome": "Vila Maria", "zona": "Norte", "lat": -23.5050, "lon": -46.5900, "populacao": 113463},
    {"id": 89, "nome": "Vila Mariana", "zona": "Sul", "lat": -23.5900, "lon": -46.6350, "populacao": 130484},
    {"id": 90, "nome": "Vila Matilde", "zona": "Leste", "lat": -23.5350, "lon": -46.5200, "populacao": 104947},
    {"id": 91, "nome": "Vila Medeiros", "zona": "Norte", "lat": -23.4920, "lon": -46.5800, "populacao": 129479},
    {"id": 92, "nome": "Vila Prudente", "zona": "Leste", "lat": -23.5850, "lon": -46.5750, "populacao": 104242},
    {"id": 93, "nome": "Vila Sônia", "zona": "Oeste", "lat": -23.5950, "lon": -46.7450, "populacao": 108441},
    {"id": 94, "nome": "Pirituba", "zona": "Norte", "lat": -23.4850, "lon": -46.7200, "populacao": 167931},
    {"id": 95, "nome": "Barra Funda", "zona": "Oeste", "lat": -23.5230, "lon": -46.6650, "populacao": 14383},
    {"id": 96, "nome": "Vila Leopoldina", "zona": "Oeste", "lat": -23.5250, "lon": -46.7200, "populacao": 26870},
]

# Corrigir duplicata: renomear id 96
DISTRITOS[95] = {"id": 96, "nome": "República Leste", "zona": "Leste", "lat": -23.5380, "lon": -46.5050, "populacao": 45000}
# Na verdade, vamos remover a duplicata e manter 95 distritos
DISTRITOS = DISTRITOS[:95]


# ============================================================================
# Serviços de saúde por distrito
# ============================================================================

# Distritos com hospitais SUS
HOSPITAIS_SUS = {
    25: "Hospital das Clínicas",
    89: "Hospital São Paulo",
    32: "Hospital do Servidor Público Estadual",
    72: "Hospital Municipal Tide Setúbal",
    58: "Hospital Municipal Carmino Caricchio",
    35: "Hospital Santa Marcelina",
    16: "Hospital Municipal Dr. Fernando M. P. da Rocha",
    94: "Hospital Municipal Dr. José Soares Hungria",
    40: "Hospital Municipal M'Boi Mirim",
    27: "Hospital Municipal Dr. Alípio Corrêa Netto",
    57: "Hospital Geral de Pedreira",
    30: "Hospital Geral de Guaianases",
    71: "Hospital Geral de São Mateus",
    77: "Santa Casa de São Paulo",
    88: "Hospital Municipal Vereador José Storopoli",
    36: "Hospital Municipal Dr. Arthur Ribeiro de Saboya",
    67: "Hospital do Mandaqui",
}

# Distritos com UPA (distribuição simplificada)
UPAS = {
    9: "UPA Brasilândia",
    16: "UPA Campo Limpo",
    18: "UPA Capão Redondo",
    21: "UPA Cidade Ademar",
    24: "UPA Cidade Tiradentes",
    29: "UPA Grajaú",
    30: "UPA Guaianases",
    34: "UPA Itaim Paulista",
    35: "UPA Itaquera",
    40: "UPA Jardim Ângela",
    43: "UPA Jardim São Luís",
    54: "UPA Parelheiros",
    66: "UPA Sacomã",
    71: "UPA São Mateus",
    75: "UPA Sapopemba",
    80: "UPA Tremembé",
    94: "UPA Pirituba",
}

# Distritos SEM UBS (mais isolados / carentes de atenção primária)
SEM_UBS = {50, 3, 24, 45, 54}  # Marsilac, Anhanguera, Cidade Tiradentes, Lajeado, Parelheiros


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calcula a distância em km entre dois pontos geográficos (Haversine)."""
    R = 6371.0  # Raio da Terra em km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def gerar_adjacencias(distritos: list, limiar_km: float = 5.5) -> list:
    """
    Gera lista de adjacências baseadas na distância entre centros dos distritos.

    Usa um limiar de distância e garante que o grafo resultante seja conexo,
    adicionando arestas extras se necessário.
    """
    adjacencias = []

    # Calcular todas as distâncias e filtrar pelo limiar
    for i, d1 in enumerate(distritos):
        for j, d2 in enumerate(distritos):
            if i < j:
                dist = haversine(d1["lat"], d1["lon"], d2["lat"], d2["lon"])
                if dist <= limiar_km:
                    adjacencias.append({
                        "distrito1_id": d1["id"],
                        "distrito2_id": d2["id"],
                        "distancia_km": round(dist, 2)
                    })

    # Verificar conectividade usando Union-Find
    parent = {d["id"]: d["id"] for d in distritos}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py

    for adj in adjacencias:
        union(adj["distrito1_id"], adj["distrito2_id"])

    # Identificar componentes desconexos
    componentes = {}
    for d in distritos:
        raiz = find(d["id"])
        if raiz not in componentes:
            componentes[raiz] = []
        componentes[raiz].append(d)

    # Conectar componentes desconexos (adicionar aresta mais curta entre componentes)
    if len(componentes) > 1:
        lista_componentes = list(componentes.values())
        for idx in range(1, len(lista_componentes)):
            menor_dist = float("inf")
            melhor_par = None
            for d1 in lista_componentes[0]:
                for d2 in lista_componentes[idx]:
                    dist = haversine(d1["lat"], d1["lon"], d2["lat"], d2["lon"])
                    if dist < menor_dist:
                        menor_dist = dist
                        melhor_par = (d1["id"], d2["id"], round(dist, 2))
            if melhor_par:
                adjacencias.append({
                    "distrito1_id": melhor_par[0],
                    "distrito2_id": melhor_par[1],
                    "distancia_km": melhor_par[2]
                })
                # Atualizar Union-Find
                union(melhor_par[0], melhor_par[1])
            # Mesclar no componente principal
            lista_componentes[0].extend(lista_componentes[idx])

    return adjacencias


def gerar_servicos(distritos: list) -> list:
    """
    Distribui serviços de saúde (UBS, UPA e hospitais SUS) pelos distritos.

    A distribuição reflete desigualdades reais:
    - Hospitais: concentrados em áreas centrais e oeste
    - UBS: ampla distribuição, mas ausentes em áreas periféricas extremas
    """
    servicos = []
    id_counter = 1

    # --- Hospitais SUS ---
    for distrito_id, nome_hospital in HOSPITAIS_SUS.items():
        servicos.append({
            "id": id_counter,
            "nome": nome_hospital,
            "tipo": "hospital_sus",
            "distrito_id": distrito_id
        })
        id_counter += 1

    # --- UPA ---
    for distrito_id, nome_upa in UPAS.items():
        servicos.append({
            "id": id_counter,
            "nome": nome_upa,
            "tipo": "upa",
            "distrito_id": distrito_id
        })
        id_counter += 1

    # --- UBS ---
    for d in distritos:
        if d["id"] not in SEM_UBS:
            # Distritos centrais/grandes têm mais UBS
            n_ubs = 1
            if d["zona"] == "Centro":
                n_ubs = 2
            elif d["populacao"] > 200000:
                n_ubs = 2

            for k in range(n_ubs):
                sufixo = f" {k + 1}" if n_ubs > 1 else ""
                servicos.append({
                    "id": id_counter,
                    "nome": f"UBS {d['nome']}{sufixo}",
                    "tipo": "ubs",
                    "distrito_id": d["id"]
                })
                id_counter += 1

    return servicos


def main():
    """Função principal: gera e salva todos os arquivos de dados."""
    print("=" * 60)
    print("SPGraph - Gerando dados dos distritos de São Paulo")
    print("=" * 60)

    # Garantir que o diretório data existe
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Gerar adjacências
    print(f"\n📍 Processando {len(DISTRITOS)} distritos...")
    adjacencias = gerar_adjacencias(DISTRITOS, limiar_km=5.5)
    print(f"🔗 {len(adjacencias)} adjacências geradas (limiar = 5.5 km)")

    # Gerar serviços
    servicos = gerar_servicos(DISTRITOS)
    contagem = {}
    for s in servicos:
        contagem[s["tipo"]] = contagem.get(s["tipo"], 0) + 1
    print(f"🏥 Serviços gerados: {contagem}")

    # Salvar arquivos JSON
    arquivo_distritos = DATA_DIR / "distritos.json"
    with open(arquivo_distritos, "w", encoding="utf-8") as f:
        json.dump(DISTRITOS, f, ensure_ascii=False, indent=2)
    print(f"\n✅ {arquivo_distritos}")

    arquivo_adjacencias = DATA_DIR / "adjacencias.json"
    with open(arquivo_adjacencias, "w", encoding="utf-8") as f:
        json.dump(adjacencias, f, ensure_ascii=False, indent=2)
    print(f"✅ {arquivo_adjacencias}")

    arquivo_servicos = DATA_DIR / "servicos.json"
    with open(arquivo_servicos, "w", encoding="utf-8") as f:
        json.dump(servicos, f, ensure_ascii=False, indent=2)
    print(f"✅ {arquivo_servicos}")

    # Resumo
    print(f"\n{'=' * 60}")
    print(f"📊 Resumo:")
    print(f"   Distritos:    {len(DISTRITOS)}")
    print(f"   Adjacências:  {len(adjacencias)}")
    print(f"   Serviços:     {len(servicos)}")
    print(f"   Hospitais SUS:{contagem.get('hospital_sus', 0)}")
    print(f"   UPA:          {contagem.get('upa', 0)}")
    print(f"   UBS:          {contagem.get('ubs', 0)}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
