
###############################################################
# 1. PACOTES
###############################################################
using HTTP
using CSV
using DataFrames
using Dates
using Statistics
using Plots

###############################################################
# 2. FUNÇÃO DE DOWNLOAD DE DADOS (YAHOO FINANCE)
###############################################################

function download_yahoo(ticker::String, start_date::Date, end_date::Date)
    period1 = Dates.value(start_date) ÷ 1000
    period2 = Dates.value(end_date) ÷ 1000

    url = "https://query1.finance.yahoo.com/v7/finance/download/$ticker?" *
          "period1=$period1&period2=$period2&interval=1d&events=history&includeAdjustedClose=true"

    response = HTTP.get(url)
    df = CSV.read(IOBuffer(response.body), DataFrame)
    return df
end

###############################################################
# 3. DEFINIÇÃO DO PERÍODO DE ANÁLISE
###############################################################
start_date = Date(2010, 1, 1)
end_date   = Date(2025, 1, 1)

###############################################################
# 4. DOWNLOAD DOS MERCADOS ACIONÁRIOS (EUA)
###############################################################
sp500   = download_yahoo("^GSPC", start_date, end_date)
nasdaq  = download_yahoo("^IXIC", start_date, end_date)
dow     = download_yahoo("^DJI",  start_date, end_date)

###############################################################
# 5. DOWNLOAD DOS MERCADOS CAMBIAIS
###############################################################
eurusd = download_yahoo("EURUSD=X", start_date, end_date)
gbpusd = download_yahoo("GBPUSD=X", start_date, end_date)
chfusd = download_yahoo("CHFUSD=X", start_date, end_date)
brlusd = download_yahoo("BRLUSD=X", start_date, end_date)
cnyusd = download_yahoo("CNYUSD=X", start_date, end_date)

###############################################################
# 6. LIMPEZA E PADRONIZAÇÃO DOS DADOS
###############################################################
# Mantém apenas data e preço ajustado
# Remove missing
# Converte datas
###############################################################
function clean_data(df::DataFrame)
    df = select(df, :Date, :AdjClose)
    dropmissing!(df)
    df.Date = Date.(df.Date)
    rename!(df, :AdjClose => :price)
    return df
end

sp500  = clean_data(sp500)
nasdaq = clean_data(nasdaq)
dow    = clean_data(dow)

eurusd = clean_data(eurusd)
gbpusd = clean_data(gbpusd)
chfusd = clean_data(chfusd)
brlusd = clean_data(brlusd)
cnyusd = clean_data(cnyusd)

###############################################################
# 7. ALINHAMENTO TEMPORAL (INNER JOIN)
###############################################################
# Garante mesma base temporal para todas as séries
###############################################################
function merge_assets(dfs::Vector{DataFrame}, names::Vector{Symbol})
    merged = dfs[1]
    rename!(merged, :price => names[1])

    for i in 2:length(dfs)
        df = dfs[i]
        rename!(df, :price => names[i])
        merged = innerjoin(merged, df, on = :Date)
    end
    return merged
end

equities = merge_assets(
    [sp500, nasdaq, dow],
    [:sp500, :nasdaq, :dow]
)

fx = merge_assets(
    [eurusd, gbpusd, chfusd, brlusd, cnyusd],
    [:eurusd, :gbpusd, :chfusd, :brlusd, :cnyusd]
)

###############################################################
# 8. TRANSFORMAÇÃO EM RETORNOS LOGARÍTMICOS
###############################################################
# Retornos = log(P_t / P_{t-1})
###############################################################
function log_returns(df::DataFrame)
    ret = DataFrame(Date = df.Date[2:end])
    for col in names(df)[2:end]
        ret[!, Symbol(col, "_ret")] =
            log.(df[2:end, col] ./ df[1:end-1, col])
    end
    return ret
end

equities_ret = log_returns(equities)
fx_ret       = log_returns(fx)

###############################################################
# 9. ESTATÍSTICAS BÁSICAS
###############################################################
# Média, desvio-padrão, mínimo, máximo
###############################################################
function summary_stats(df::DataFrame)
    stats = DataFrame(
        asset = String[],
        mean = Float64[],
        std = Float64[],
        min = Float64[],
        max = Float64[]
    )

    for col in names(df)[2:end]
        push!(stats, (
            string(col),
            mean(df[!, col]),
            std(df[!, col]),
            minimum(df[!, col]),
            maximum(df[!, col])
        ))
    end
    return stats
end

stats_equities = summary_stats(equities_ret)
stats_fx       = summary_stats(fx_ret)

###############################################################
# 10. MATRIZ DE CORRELAÇÃO
###############################################################
corr_equities = cor(Matrix(select(equities_ret, Not(:Date))))
corr_fx       = cor(Matrix(select(fx_ret, Not(:Date))))

###############################################################
# 11. VOLATILIDADE (DESVIO-PADRÃO DOS RETORNOS)
###############################################################
vol_equities = std.(eachcol(select(equities_ret, Not(:Date))))
vol_fx       = std.(eachcol(select(fx_ret, Not(:Date))))

###############################################################
# 12. GRÁFICOS – RETORNOS DOS ÍNDICES
###############################################################
plot(
    equities_ret.Date,
    equities_ret.sp500_ret,
    label = "S&P 500",
    title = "Retornos Logarítmicos – Mercados Acionários",
    legend = :bottomright
)
plot!(equities_ret.Date, equities_ret.nasdaq_ret, label = "NASDAQ")
plot!(equities_ret.Date, equities_ret.dow_ret, label = "DOW")

###############################################################
# 13. GRÁFICOS – RETORNOS CAMBIAIS
###############################################################
plot(
    fx_ret.Date,
    fx_ret.eurusd_ret,
    label = "EUR/USD",
    title = "Retornos Logarítmicos – Mercados Cambiais",
    legend = :bottomright
)
plot!(fx_ret.Date, fx_ret.gbpusd_ret, label = "GBP/USD")
plot!(fx_ret.Date, fx_ret.chfusd_ret, label = "CHF/USD")
plot!(fx_ret.Date, fx_ret.brlusd_ret, label = "BRL/USD")
plot!(fx_ret.Date, fx_ret.cnyusd_ret, label = "CNY/USD")

###############################################################
# 14. OUTPUT FINAL (PARA ANÁLISE NO TCC)
###############################################################
println("=== ESTATÍSTICAS – MERCADOS ACIONÁRIOS ===")
println(stats_equities)

println("\n=== ESTATÍSTICAS – MERCADOS CAMBIAIS ===")
println(stats_fx)

println("\n=== CORRELAÇÃO – EQUITIES ===")
println(corr_equities)

println("\n=== CORRELAÇÃO – FX ===")
println(corr_fx)

println("\n=== VOLATILIDADE – EQUITIES ===")
println(vol_equities)

println("\n=== VOLATILIDADE – FX ===")
println(vol_fx)

###############################################################
# FIM DO PIPELINE
# Pesquisa empírica feita integralmente via programação
# Resultados derivados diretamente do código
# Base pronta para Payroll Economics e modelos macro
###############################################################
