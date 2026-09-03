# Comparador PSVT

Ferramenta de página única para substituir a conferência linha a linha de duas
planilhas mensais do PSVT. Confronta o **arquivo anterior** com o **arquivo atual**
usando duas colunas, lidas pela posição real na planilha:

| Coluna | Conteúdo             | Índice |
|--------|----------------------|--------|
| `N`    | Número da instalação | 14ª    |
| `Y`    | Compensação mensal   | 25ª    |

## Regras da comparação

- Instalação **no anterior e não no atual** → *compensação cessada*.
- Instalação **não no anterior e no atual** → *nova compensação iniciada*.
- Instalação **nos dois arquivos** → *mantida*, com a variação de compensação entre os meses.

## Como usar

Abra `index.html` no navegador (duplo clique já basta — não precisa de servidor)
e arraste os dois `.xlsx`. Enquanto nenhum arquivo é carregado, a página mostra
dados de exemplo, sinalizados como tal, para que o formato do resultado fique claro.

Os arquivos são lidos inteiramente no navegador; nada é enviado para fora da máquina.
A leitura do `.xlsx` usa SheetJS via CDN, então a primeira abertura precisa de internet.

## Ajustes disponíveis

- **Aba** da planilha e **primeira linha de dados** (detectada automaticamente, editável).
- **Colunas** de instalação e de compensação, caso o layout do relatório mude.
- **Unidade** exibida (kWh, R$ ou nenhuma).
- **Zeros à esquerda**: ignorados por padrão, porque o Excel costuma gravar a mesma
  instalação ora como número, ora como texto — o que faria a mesma UC parecer
  cessada em um arquivo e nova no outro.

## Saída

- Indicadores: cessadas, novas, mantidas e compensação total.
- Gráfico de composição da carteira nos dois arquivos.
- Ponte (waterfall) mostrando como o total anterior chega ao total atual.
- Abas com tabelas ordenáveis e filtráveis, exportáveis em CSV (separador `;`, UTF-8 com BOM,
  pronto para o Excel em português) ou copiáveis direto para uma planilha.
- Aba **Inconsistências**: instalação repetida no mesmo arquivo (os valores são somados),
  compensação não numérica e compensação sem número de instalação.

## Arquivo autônomo para testes

`dist/comparador-psvt-offline.html` é um único arquivo com a biblioteca de leitura
embutida: baixe, dê um duplo clique e use — sem internet, sem instalação, sem servidor.
É a versão indicada para distribuir para a equipe.

`index.html` é a fonte editável e carrega a biblioteca por CDN. Depois de alterá-la,
regenere o arquivo autônomo com:

```
python3 build.py
```

A pasta `exemplos/` traz duas planilhas de teste no formato do relatório
(cabeçalho na linha 4, dados a partir da linha 5) que exercitam os casos difíceis:
instalação gravada com zero à esquerda em um mês e como número no outro, valor em
texto (`340,00` e `R$ 1.004,80`), instalação repetida com rateio parcial, valor não
numérico e linha com compensação sem número de instalação.

Resultado esperado com esses dois arquivos: 3 cessadas, 5 novas, 9 mantidas
e 3 inconsistências.

Biblioteca embutida: [SheetJS](https://sheetjs.com) 0.18.5, Apache-2.0
(`vendor/xlsx-LICENSE.txt`).
