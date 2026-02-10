############################
# DEPENDÊNCIAS
############################
using CSV
using DataFrames
using Dates
using Statistics
using Plots
using Downloads

############################
# DOWNLOAD DE DADOS (STOOQ)
############################
function download_stooq(symbol::String)
    url = "https://stooq.pl/q/d/l/?s=$(lowercase(symbol))&i=d"
    file = Downloads.download(url)
    return CSV.read(file, DataFrame)
end

############################
# DADOS – ÍNDICES
############################
sp500  = download_stooq("spx")
nasdaq = download_stooq("ixic")
dow    = download_stooq("djia")

############################
# DADOS – CÂMBIO
############################
eurusd = download_stooq("eurusd")
gbpusd = download_stooq("gbpusd")
chfusd = download_stooq("chfusd")
brlusd = download_stooq("brlusd")
cnyusd = download_stooq("cnyusd")

############################
# LIMPEZA
############################
function clean_data(df::DataFrame)
    df = select(df, :Date, :Close)
    dropmissing!(df)
    df.Date = Date.(df.Date)
    rename!(df, :Close => :price)
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

############################
# MERGE TEMPORAL
############################
function merge_assets(dfs::Vector{DataFrame}, names::Vector{Symbol})
    out = dfs[1]
    rename!(out, :price => names[1])

    for i in 2:length(dfs)
        df = dfs[i]
        rename!(df, :price => names[i])
        out = innerjoin(out, df, on = :Date)
    end
    return out
end

equities = merge_assets(
    [sp500, nasdaq, dow],
    [:sp500, :nasdaq, :dow]
)

fx = merge_assets(
    [eurusd, gbpusd, chfusd, brlusd, cnyusd],
    [:eurusd, :gbpusd, :chfusd, :brlusd, :cnyusd]
)

############################
# RETORNOS LOG
############################
function log_returns(df::DataFrame)
    ret = DataFrame(Date = df.Date[2:end])
    for c in names(df)[2:end]
        ret[!, Symbol(c, "_ret")] =
            log.(df[2:end, c] ./ df[1:end-1, c])
    end
    return ret
end

equities_ret = log_returns(equities)
fx_ret       = log_returns(fx)

############################
# ESTATÍSTICAS
############################
function summary_stats(df::DataFrame)
    out = DataFrame(
        asset = String[],
        mean  = Float64[],
        std   = Float64[],
        min   = Float64[],
        max   = Float64[]
    )

    for c in names(df)[2:end]
        push!(out, (
            string(c),
            mean(df[!, c]),
            std(df[!, c]),
            minimum(df[!, c]),
            maximum(df[!, c])
        ))
    end
    return out
end

stats_equities = summary_stats(equities_ret)
stats_fx       = summary_stats(fx_ret)

############################
# CORRELAÇÃO
############################
corr_equities = cor(Matrix(select(equities_ret, Not(:Date))))
corr_fx       = cor(Matrix(select(fx_ret, Not(:Date))))

############################
# VOLATILIDADE
############################
vol_equities = std.(eachcol(select(equities_ret, Not(:Date))))
vol_fx       = std.(eachcol(select(fx_ret, Not(:Date))))

############################
# GRÁFICOS
############################
plot(equities_ret.Date, equities_ret.sp500_ret, label="SP500")
plot!(equities_ret.Date, equities_ret.nasdaq_ret, label="NASDAQ")
plot!(equities_ret.Date, equities_ret.dow_ret, label="DOW")

plot(fx_ret.Date, fx_ret.eurusd_ret, label="EURUSD")
plot!(fx_ret.Date, fx_ret.gbpusd_ret, label="GBPUSD")
plot!(fx_ret.Date, fx_ret.chfusd_ret, label="CHFUSD")
plot!(fx_ret.Date, fx_ret.brlusd_ret, label="BRLUSD")
plot!(fx_ret.Date, fx_ret.cnyusd_ret, label="CNYUSD")

############################
# OUTPUT
############################
println(stats_equities)
println(stats_fx)
println(corr_equities)
println(corr_fx)
println(vol_equities)
println(vol_fx)
############################
# DEPENDÊNCIAS
############################
using CSV
using DataFrames
using Dates
using Statistics
using Plots
using Downloads

############################
# DOWNLOAD DE DADOS (STOOQ)
############################
function download_stooq(symbol::String)
    url = "https://stooq.pl/q/d/l/?s=$(lowercase(symbol))&i=d"
    file = Downloads.download(url)
    return CSV.read(file, DataFrame)
end

############################
# DADOS – ÍNDICES
############################
sp500  = download_stooq("spx")
nasdaq = download_stooq("ixic")
dow    = download_stooq("djia")

############################
# DADOS – CÂMBIO
############################
eurusd = download_stooq("eurusd")
gbpusd = download_stooq("gbpusd")
chfusd = download_stooq("chfusd")
brlusd = download_stooq("brlusd")
cnyusd = download_stooq("cnyusd")

############################
# LIMPEZA
############################
function clean_data(df::DataFrame)
    df = select(df, :Date, :Close)
    dropmissing!(df)
    df.Date = Date.(df.Date)
    rename!(df, :Close => :price)
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

############################
# MERGE TEMPORAL
############################
function merge_assets(dfs::Vector{DataFrame}, names::Vector{Symbol})
    out = dfs[1]
    rename!(out, :price => names[1])

    for i in 2:length(dfs)
        df = dfs[i]
        rename!(df, :price => names[i])
        out = innerjoin(out, df, on = :Date)
    end
    return out
end

equities = merge_assets(
    [sp500, nasdaq, dow],
    [:sp500, :nasdaq, :dow]
)

fx = merge_assets(
    [eurusd, gbpusd, chfusd, brlusd, cnyusd],
    [:eurusd, :gbpusd, :chfusd, :brlusd, :cnyusd]
)

############################
# RETORNOS LOG
############################
function log_returns(df::DataFrame)
    ret = DataFrame(Date = df.Date[2:end])
    for c in names(df)[2:end]
        ret[!, Symbol(c, "_ret")] =
            log.(df[2:end, c] ./ df[1:end-1, c])
    end
    return ret
end

equities_ret = log_returns(equities)
fx_ret       = log_returns(fx)

############################
# ESTATÍSTICAS
############################
function summary_stats(df::DataFrame)
    out = DataFrame(
        asset = String[],
        mean  = Float64[],
        std   = Float64[],
        min   = Float64[],
        max   = Float64[]
    )

    for c in names(df)[2:end]
        push!(out, (
            string(c),
            mean(df[!, c]),
            std(df[!, c]),
            minimum(df[!, c]),
            maximum(df[!, c])
        ))
    end
    return out
end

stats_equities = summary_stats(equities_ret)
stats_fx       = summary_stats(fx_ret)

############################
# CORRELAÇÃO
############################
corr_equities = cor(Matrix(select(equities_ret, Not(:Date))))
corr_fx       = cor(Matrix(select(fx_ret, Not(:Date))))

############################
# VOLATILIDADE
############################
vol_equities = std.(eachcol(select(equities_ret, Not(:Date))))
vol_fx       = std.(eachcol(select(fx_ret, Not(:Date))))

############################
# GRÁFICOS
############################
plot(equities_ret.Date, equities_ret.sp500_ret, label="SP500")
plot!(equities_ret.Date, equities_ret.nasdaq_ret, label="NASDAQ")
plot!(equities_ret.Date, equities_ret.dow_ret, label="DOW")

plot(fx_ret.Date, fx_ret.eurusd_ret, label="EURUSD")
plot!(fx_ret.Date, fx_ret.gbpusd_ret, label="GBPUSD")
plot!(fx_ret.Date, fx_ret.chfusd_ret, label="CHFUSD")
plot!(fx_ret.Date, fx_ret.brlusd_ret, label="BRLUSD")
plot!(fx_ret.Date, fx_ret.cnyusd_ret, label="CNYUSD")

############################
# OUTPUT
############################
println(stats_equities)
println(stats_fx)
println(corr_equities)
println(corr_fx)
println(vol_equities)
println(vol_fx)
############################
# DEPENDÊNCIAS
############################
using CSV
using DataFrames
using Dates
using Statistics
using Plots
using Downloads

############################
# DOWNLOAD DE DADOS (STOOQ)
############################
function download_stooq(symbol::String)
    url = "https://stooq.pl/q/d/l/?s=$(lowercase(symbol))&i=d"
    file = Downloads.download(url)
    return CSV.read(file, DataFrame)
end

############################
# DADOS – ÍNDICES
############################
sp500  = download_stooq("spx")
nasdaq = download_stooq("ixic")
dow    = download_stooq("djia")

############################
# DADOS – CÂMBIO
############################
eurusd = download_stooq("eurusd")
gbpusd = download_stooq("gbpusd")
chfusd = download_stooq("chfusd")
brlusd = download_stooq("brlusd")
cnyusd = download_stooq("cnyusd")

############################
# LIMPEZA
############################
function clean_data(df::DataFrame)
    df = select(df, :Date, :Close)
    dropmissing!(df)
    df.Date = Date.(df.Date)
    rename!(df, :Close => :price)
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

############################
# MERGE TEMPORAL
############################
function merge_assets(dfs::Vector{DataFrame}, names::Vector{Symbol})
    out = dfs[1]
    rename!(out, :price => names[1])

    for i in 2:length(dfs)
        df = dfs[i]
        rename!(df, :price => names[i])
        out = innerjoin(out, df, on = :Date)
    end
    return out
end

equities = merge_assets(
    [sp500, nasdaq, dow],
    [:sp500, :nasdaq, :dow]
)

fx = merge_assets(
    [eurusd, gbpusd, chfusd, brlusd, cnyusd],
    [:eurusd, :gbpusd, :chfusd, :brlusd, :cnyusd]
)

############################
# RETORNOS LOG
############################
function log_returns(df::DataFrame)
    ret = DataFrame(Date = df.Date[2:end])
    for c in names(df)[2:end]
        ret[!, Symbol(c, "_ret")] =
            log.(df[2:end, c] ./ df[1:end-1, c])
    end
    return ret
end

equities_ret = log_returns(equities)
fx_ret       = log_returns(fx)

############################
# ESTATÍSTICAS
############################
function summary_stats(df::DataFrame)
    out = DataFrame(
        asset = String[],
        mean  = Float64[],
        std   = Float64[],
        min   = Float64[],
        max   = Float64[]
    )

    for c in names(df)[2:end]
        push!(out, (
            string(c),
            mean(df[!, c]),
            std(df[!, c]),
            minimum(df[!, c]),
            maximum(df[!, c])
        ))
    end
    return out
end

stats_equities = summary_stats(equities_ret)
stats_fx       = summary_stats(fx_ret)

############################
# CORRELAÇÃO
############################
corr_equities = cor(Matrix(select(equities_ret, Not(:Date))))
corr_fx       = cor(Matrix(select(fx_ret, Not(:Date))))

############################
# VOLATILIDADE
############################
vol_equities = std.(eachcol(select(equities_ret, Not(:Date))))
vol_fx       = std.(eachcol(select(fx_ret, Not(:Date))))

############################
# GRÁFICOS
############################
plot(equities_ret.Date, equities_ret.sp500_ret, label="SP500")
plot!(equities_ret.Date, equities_ret.nasdaq_ret, label="NASDAQ")
plot!(equities_ret.Date, equities_ret.dow_ret, label="DOW")

plot(fx_ret.Date, fx_ret.eurusd_ret, label="EURUSD")
plot!(fx_ret.Date, fx_ret.gbpusd_ret, label="GBPUSD")
plot!(fx_ret.Date, fx_ret.chfusd_ret, label="CHFUSD")
plot!(fx_ret.Date, fx_ret.brlusd_ret, label="BRLUSD")
plot!(fx_ret.Date, fx_ret.cnyusd_ret, label="CNYUSD")

############################
# OUTPUT
############################
println(stats_equities)
println(stats_fx)
println(corr_equities)
println(corr_fx)
println(vol_equities)
println(vol_fx)
############################
# DEPENDÊNCIAS
############################
using CSV
using DataFrames
using Dates
using Statistics
using Plots
using Downloads

############################
# DOWNLOAD DE DADOS (STOOQ)
############################
function download_stooq(symbol::String)
    url = "https://stooq.pl/q/d/l/?s=$(lowercase(symbol))&i=d"
    file = Downloads.download(url)
    return CSV.read(file, DataFrame)
end

############################
# DADOS – ÍNDICES
############################
sp500  = download_stooq("spx")
nasdaq = download_stooq("ixic")
dow    = download_stooq("djia")

############################
# DADOS – CÂMBIO
############################
eurusd = download_stooq("eurusd")
gbpusd = download_stooq("gbpusd")
chfusd = download_stooq("chfusd")
brlusd = download_stooq("brlusd")
cnyusd = download_stooq("cnyusd")

############################
# LIMPEZA
############################
function clean_data(df::DataFrame)
    df = select(df, :Date, :Close)
    dropmissing!(df)
    df.Date = Date.(df.Date)
    rename!(df, :Close => :price)
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

############################
# MERGE TEMPORAL
############################
function merge_assets(dfs::Vector{DataFrame}, names::Vector{Symbol})
    out = dfs[1]
    rename!(out, :price => names[1])

    for i in 2:length(dfs)
        df = dfs[i]
        rename!(df, :price => names[i])
        out = innerjoin(out, df, on = :Date)
    end
    return out
end

equities = merge_assets(
    [sp500, nasdaq, dow],
    [:sp500, :nasdaq, :dow]
)

fx = merge_assets(
    [eurusd, gbpusd, chfusd, brlusd, cnyusd],
    [:eurusd, :gbpusd, :chfusd, :brlusd, :cnyusd]
)

############################
# RETORNOS LOG
############################
function log_returns(df::DataFrame)
    ret = DataFrame(Date = df.Date[2:end])
    for c in names(df)[2:end]
        ret[!, Symbol(c, "_ret")] =
            log.(df[2:end, c] ./ df[1:end-1, c])
    end
    return ret
end

equities_ret = log_returns(equities)
fx_ret       = log_returns(fx)

############################
# ESTATÍSTICAS
############################
function summary_stats(df::DataFrame)
    out = DataFrame(
        asset = String[],
        mean  = Float64[],
        std   = Float64[],
        min   = Float64[],
        max   = Float64[]
    )

    for c in names(df)[2:end]
        push!(out, (
            string(c),
            mean(df[!, c]),
            std(df[!, c]),
            minimum(df[!, c]),
            maximum(df[!, c])
        ))
    end
    return out
end

stats_equities = summary_stats(equities_ret)
stats_fx       = summary_stats(fx_ret)

############################
# CORRELAÇÃO
############################
corr_equities = cor(Matrix(select(equities_ret, Not(:Date))))
corr_fx       = cor(Matrix(select(fx_ret, Not(:Date))))

############################
# VOLATILIDADE
############################
vol_equities = std.(eachcol(select(equities_ret, Not(:Date))))
vol_fx       = std.(eachcol(select(fx_ret, Not(:Date))))

############################
# GRÁFICOS
############################
plot(equities_ret.Date, equities_ret.sp500_ret, label="SP500")
plot!(equities_ret.Date, equities_ret.nasdaq_ret, label="NASDAQ")
plot!(equities_ret.Date, equities_ret.dow_ret, label="DOW")

plot(fx_ret.Date, fx_ret.eurusd_ret, label="EURUSD")
plot!(fx_ret.Date, fx_ret.gbpusd_ret, label="GBPUSD")
plot!(fx_ret.Date, fx_ret.chfusd_ret, label="CHFUSD")
plot!(fx_ret.Date, fx_ret.brlusd_ret, label="BRLUSD")
plot!(fx_ret.Date, fx_ret.cnyusd_ret, label="CNYUSD")

############################
# OUTPUT
############################
println(stats_equities)
println(stats_fx)
println(corr_equities)
println(corr_fx)
println(vol_equities)
println(vol_fx)
############################
# DEPENDÊNCIAS
############################
using CSV
using DataFrames
using Dates
using Statistics
using Plots
using Downloads

############################
# DOWNLOAD DE DADOS (STOOQ)
############################
function download_stooq(symbol::String)
    url = "https://stooq.pl/q/d/l/?s=$(lowercase(symbol))&i=d"
    file = Downloads.download(url)
    return CSV.read(file, DataFrame)
end

############################
# DADOS – ÍNDICES
############################
sp500  = download_stooq("spx")
nasdaq = download_stooq("ixic")
dow    = download_stooq("djia")

############################
# DADOS – CÂMBIO
############################
eurusd = download_stooq("eurusd")
gbpusd = download_stooq("gbpusd")
chfusd = download_stooq("chfusd")
brlusd = download_stooq("brlusd")
cnyusd = download_stooq("cnyusd")

############################
# LIMPEZA
############################
function clean_data(df::DataFrame)
    df = select(df, :Date, :Close)
    dropmissing!(df)
    df.Date = Date.(df.Date)
    rename!(df, :Close => :price)
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

############################
# MERGE TEMPORAL
############################
function merge_assets(dfs::Vector{DataFrame}, names::Vector{Symbol})
    out = dfs[1]
    rename!(out, :price => names[1])

    for i in 2:length(dfs)
        df = dfs[i]
        rename!(df, :price => names[i])
        out = innerjoin(out, df, on = :Date)
    end
    return out
end

equities = merge_assets(
    [sp500, nasdaq, dow],
    [:sp500, :nasdaq, :dow]
)

fx = merge_assets(
    [eurusd, gbpusd, chfusd, brlusd, cnyusd],
    [:eurusd, :gbpusd, :chfusd, :brlusd, :cnyusd]
)

############################
# RETORNOS LOG
############################
function log_returns(df::DataFrame)
    ret = DataFrame(Date = df.Date[2:end])
    for c in names(df)[2:end]
        ret[!, Symbol(c, "_ret")] =
            log.(df[2:end, c] ./ df[1:end-1, c])
    end
    return ret
end

equities_ret = log_returns(equities)
fx_ret       = log_returns(fx)

############################
# ESTATÍSTICAS
############################
function summary_stats(df::DataFrame)
    out = DataFrame(
        asset = String[],
        mean  = Float64[],
        std   = Float64[],
        min   = Float64[],
        max   = Float64[]
    )

    for c in names(df)[2:end]
        push!(out, (
            string(c),
            mean(df[!, c]),
            std(df[!, c]),
            minimum(df[!, c]),
            maximum(df[!, c])
        ))
    end
    return out
end

stats_equities = summary_stats(equities_ret)
stats_fx       = summary_stats(fx_ret)

############################
# CORRELAÇÃO
############################
corr_equities = cor(Matrix(select(equities_ret, Not(:Date))))
corr_fx       = cor(Matrix(select(fx_ret, Not(:Date))))

############################
# VOLATILIDADE
############################
vol_equities = std.(eachcol(select(equities_ret, Not(:Date))))
vol_fx       = std.(eachcol(select(fx_ret, Not(:Date))))

############################
# GRÁFICOS
############################
gr()

p1 = plot(
    equities_ret.Date,
    equities_ret.sp500_ret,
    label = "SP500",
    legend = :top
)
plot!(p1, equities_ret.Date, equities_ret.nasdaq_ret, label = "NASDAQ")
plot!(p1, equities_ret.Date, equities_ret.dow_ret, label = "DOW")
display(p1)

p2 = plot(
    fx_ret.Date,
    fx_ret.eurusd_ret,
    label = "EURUSD",
    legend = :top
)
plot!(p2, fx_ret.Date, fx_ret.gbpusd_ret, label = "GBPUSD")
plot!(p2, fx_ret.Date, fx_ret.chfusd_ret, label = "CHFUSD")
plot!(p2, fx_ret.Date, fx_ret.brlusd_ret, label = "BRLUSD")
plot!(p2, fx_ret.Date, fx_ret.cnyusd_ret, label = "CNYUSD")
display(p2)

############################
# OUTPUT
############################
println(stats_equities)
println(stats_fx)
println(corr_equities)
println(corr_fx)
println(vol_equities)
println(vol_fx)
