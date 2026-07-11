import json
import os
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'produtos.json')

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/produtos', methods=['GET'])
def get_produtos():
    try:
        data = load_data()
        return jsonify(data.get('produtos', []))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/produtos', methods=['POST'])
def add_produto():
    try:
        produto = request.json
        data = load_data()
        produtos = data.get('produtos', [])
        
        novo_id = max([p['id'] for p in produtos], default=0) + 1
        produto['id'] = novo_id
        
        # Ensure it has necessary fields
        if 'nome' not in produto or 'preco_medio' not in produto:
            return jsonify({'error': 'Nome e Preço são obrigatórios'}), 400
            
        produtos.append(produto)
        data['produtos'] = produtos
        save_data(data)
        
        return jsonify(produto), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/produtos/<int:id>', methods=['DELETE'])
def delete_produto(id):
    try:
        data = load_data()
        produtos = data.get('produtos', [])
        
        for i, p in enumerate(produtos):
            if p['id'] == id:
                produtos.pop(i)
                data['produtos'] = produtos
                save_data(data)
                return jsonify({'success': True})
                
        return jsonify({'error': 'Produto não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cupom', methods=['POST'])
def gerar_cupom():
    try:
        req_data = request.json
        carrinho = req_data.get('carrinho', [])
        forma_pagamento = req_data.get('forma_pagamento', 'Dinheiro')
        cpf_consumidor = req_data.get('cpf', 'CONSUMIDOR NÃO IDENTIFICADO')
        
        total = sum(item['subtotal'] for item in carrinho)
        tributos = total * 0.1825
        
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cupom_fiscal.html')
        import datetime
        import random
        data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        chave_acesso = " ".join([str(random.randint(1000, 9999)) for _ in range(11)])
        protocolo = f"{random.randint(100000000, 999999999)} - {data_hora}"
        
        troco = 0.0
        pago = total
        if forma_pagamento == 'Dinheiro':
            if total < 10:
                pago = 10.0
            elif total < 20:
                pago = 20.0
            elif total < 50:
                pago = 50.0
            elif total < 100:
                pago = 100.0
            else:
                pago = float(int(total / 50) + 1) * 50.0
            troco = pago - total

        html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>NFC-e - Cupom Fiscal Eletrônico</title>
    <link href="https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&family=Outfit:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        body {{
            background: radial-gradient(circle at center, #181922 0%, #090a0f 100%);
            color: #1e293b;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 60px 20px;
            font-family: 'Courier Prime', monospace;
            font-size: 12px;
            min-height: 100vh;
            margin: 0;
        }}
        .receipt-card {{
            background: #faf9f5;
            width: 390px;
            padding: 45px 32px;
            box-shadow: 
                0 30px 70px -15px rgba(0, 0, 0, 0.8),
                0 15px 30px -10px rgba(0, 0, 0, 0.4);
            position: relative;
            /* Jagged top and bottom edges using modern CSS clip-path */
            clip-path: polygon(
                0% 12px, 2.5% 0px, 5% 12px, 7.5% 0px, 10% 12px, 12.5% 0px, 15% 12px, 17.5% 0px, 20% 12px, 22.5% 0px, 25% 12px, 27.5% 0px, 30% 12px, 32.5% 0px, 35% 12px, 37.5% 0px, 40% 12px, 42.5% 0px, 45% 12px, 47.5% 0px, 50% 12px, 52.5% 0px, 55% 12px, 57.5% 0px, 60% 12px, 62.5% 0px, 65% 12px, 67.5% 0px, 70% 12px, 72.5% 0px, 75% 12px, 77.5% 0px, 80% 12px, 82.5% 0px, 85% 12px, 87.5% 0px, 90% 12px, 92.5% 0px, 95% 12px, 97.5% 0px, 100% 12px,
                100% calc(100% - 12px), 97.5% 100%, 95% calc(100% - 12px), 92.5% 100%, 90% calc(100% - 12px), 87.5% 100%, 85% calc(100% - 12px), 82.5% 100%, 80% calc(100% - 12px), 77.5% 100%, 75% calc(100% - 12px), 72.5% 100%, 70% calc(100% - 12px), 67.5% 100%, 65% calc(100% - 12px), 62.5% 100%, 60% calc(100% - 12px), 57.5% 100%, 55% calc(100% - 12px), 52.5% 100%, 50% calc(100% - 12px), 47.5% 100%, 45% calc(100% - 12px), 42.5% 100%, 40% calc(100% - 12px), 37.5% 100%, 35% calc(100% - 12px), 32.5% 100%, 30% calc(100% - 12px), 27.5% 100%, 25% calc(100% - 12px), 22.5% 100%, 20% calc(100% - 12px), 17.5% 100%, 15% calc(100% - 12px), 12.5% 100%, 10% calc(100% - 12px), 7.5% 100%, 5% calc(100% - 12px), 2.5% 100%, 0% calc(100% - 12px)
            );
        
        .header {{
            text-align: center;
            border-bottom: 2px dashed #cbd5e1;
            padding-bottom: 22px;
            margin-bottom: 20px;
        }}
        .header h1 {{
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: 1.8rem;
            margin: 0 0 6px 0;
            color: #0f172a;
            letter-spacing: -0.5px;
        }}
        .header p {{
            margin: 3px 0;
            color: #475569;
            font-size: 10px;
            font-weight: bold;
        }}
        .document-title {{
            font-weight: bold;
            font-size: 11px;
            letter-spacing: 0.5px;
            color: #334155;
            margin-top: 15px;
            text-transform: uppercase;
        }}
        .table-items {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 15px;
        }}
        .table-items th {{
            text-align: left;
            color: #475569;
            border-bottom: 2px solid #334155;
            padding-bottom: 8px;
            font-size: 11px;
            text-transform: uppercase;
            font-weight: bold;
        }}
        .table-items td {{
            padding: 10px 0;
            vertical-align: top;
            color: #0f172a;
            border-bottom: 1px dashed #e2e8f0;
        }}
        .item-details {{
            color: #64748b;
            font-size: 10px;
            margin-top: 3px;
        }}
        .divider {{
            border-top: 2px dashed #cbd5e1;
            margin: 18px 0;
        }}
        .summary-section {{
            display: flex;
            flex-direction: column;
            gap: 6px;
            font-size: 11px;
            color: #334155;
        }}
        .summary-row {{
            display: flex;
            justify-content: space-between;
        }}
        .total-row {{
            font-size: 18px;
            font-weight: bold;
            color: #0f172a;
            margin: 12px 0;
            border-top: 2px solid #334155;
            border-bottom: 2px solid #334155;
            padding: 10px 0;
            display: flex;
            justify-content: space-between;
        }}
        .tax-info {{
            font-size: 9px;
            color: #64748b;
            text-align: center;
            margin-top: 18px;
            line-height: 1.4;
        }}
        .access-key {{
            word-break: break-all;
            text-align: center;
            background: #f1f5f9;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 10px;
            font-size: 10px;
            color: #334155;
            margin: 18px 0;
            line-height: 1.5;
        }}
        .barcode-svg {{
            display: block;
            margin: 15px auto;
            max-width: 100%;
        }}
        .qrcode-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 22px 0;
            gap: 8px;
        }}
        .qrcode-svg {{
            width: 130px;
            height: 130px;
            background: white;
            padding: 6px;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
        }}
        .footer {{
            text-align: center;
            color: #475569;
            font-size: 11px;
            margin-top: 25px;
            border-top: 2px dashed #cbd5e1;
            padding-top: 18px;
            line-height: 1.5;
        }}
        
        @media print {{
            body {{
                background: #fff;
                color: #000;
                padding: 0;
            }}
            .receipt-card {{
                box-shadow: none;
                border: none;
                width: 100%;
                max-width: 80mm;
                padding: 0;
                background: #fff;
                clip-path: none;
            }}
        }}
    </style>
</head>
<body onload="window.print()">
    <div class="receipt-card">
        <div class="header">
            <h1>SuperPython</h1>
            <p>SUPERMERCADO PYTHON LTDA</p>
            <p>CNPJ: 12.345.678/0001-99 | IE: 111.222.333.444</p>
            <p>AV. DA TECNOLOGIA, 1024, SÃO PAULO - SP</p>
            <div class="document-title">Documento Auxiliar da Nota Fiscal de Consumidor Eletrônica</div>
        </div>

        <table class="table-items">
            <thead>
                <tr>
                    <th>Item / Descrição</th>
                    <th style="text-align: center;">Qtd x Unit</th>
                    <th style="text-align: right;">Total</th>
                </tr>
            </thead>
            <tbody>
"""
        for i, item in enumerate(carrinho):
            prod = item['produto']
            html_content += f"""
                <tr class="item-row">
                    <td>
                        <strong>{i+1:03d} | {prod['nome']}</strong>
                        <div class="item-details">Cód: {prod['id']} | Cat: {prod['categoria']}</div>
                    </td>
                    <td style="text-align: center; vertical-align: middle; white-space: nowrap;">
                        {item['qtd']} {prod['unidade']} x R$ {prod['preco_medio']:.2f}
                    </td>
                    <td style="text-align: right; vertical-align: middle; font-weight: bold;">
                        R$ {item['subtotal']:.2f}
                    </td>
                </tr>
            """
            
        html_content += f"""
            </tbody>
        </table>

        <div class="summary-section">
            <div class="summary-row">
                <span>Qtd. Total de Itens:</span>
                <span>{sum(item['qtd'] for item in carrinho)}</span>
            </div>
            <div class="summary-row">
                <span>Valor Bruto:</span>
                <span>R$ {total:.2f}</span>
            </div>
            <div class="total-row">
                <span>VALOR A PAGAR:</span>
                <span>R$ {total:.2f}</span>
            </div>
            <div class="summary-row" style="font-weight: bold;">
                <span>Forma de Pagamento:</span>
                <span>{forma_pagamento}</span>
            </div>
            <div class="summary-row">
                <span>Valor Pago:</span>
                <span>R$ {pago:.2f}</span>
            </div>
            <div class="summary-row" style="color: #64748b;">
                <span>Troco:</span>
                <span>R$ {troco:.2f}</span>
            </div>
        </div>

        <div class="divider"></div>
        
        <div class="summary-section">
            <div class="summary-row" style="font-size: 10px;">
                <span>CPF do Consumidor:</span>
                <span>{cpf_consumidor}</span>
            </div>
            <div class="summary-row" style="font-size: 10px;">
                <span>NFC-e Nº:</span>
                <span>{random.randint(100000, 999999):06d} | Série: 001</span>
            </div>
            <div class="summary-row" style="font-size: 10px;">
                <span>Emissão:</span>
                <span>{data_hora}</span>
            </div>
            <div class="summary-row" style="font-size: 10px;">
                <span>Via Consumidor</span>
                <span>Protocolo: {protocolo}</span>
            </div>
        </div>

        <div class="access-key">
            <strong>CHAVE DE ACESSO</strong><br>
            {chave_acesso}
        </div>

        <!-- Simulated Barcode -->
        <svg class="barcode-svg" width="300" height="40" viewBox="0 0 300 40">
            <rect width="300" height="40" fill="transparent"/>
            {"".join(f'<rect x="{x}" y="5" width="{random.choice([1, 2, 3])}" height="30" fill="#1e293b"/>' for x in range(15, 285, random.choice([3, 4, 5])))}
        </svg>

        <div class="qrcode-container">
            <span style="font-size: 10px; color: #475569; font-weight: bold; margin-bottom: 5px;">Consulta via Leitor de QR Code</span>
            <!-- Simulated QR Code SVG -->
            <svg class="qrcode-svg" viewBox="0 0 100 100">
                <rect width="100" height="100" fill="white"/>
                <rect x="5" y="5" width="20" height="20" fill="black"/>
                <rect x="8" y="8" width="14" height="14" fill="white"/>
                <rect x="11" y="11" width="8" height="8" fill="black"/>
                
                <rect x="75" y="5" width="20" height="20" fill="black"/>
                <rect x="78" y="8" width="14" height="14" fill="white"/>
                <rect x="81" y="11" width="8" height="8" fill="black"/>
                
                <rect x="5" y="75" width="20" height="20" fill="black"/>
                <rect x="8" y="78" width="14" height="14" fill="white"/>
                <rect x="11" y="81" width="8" height="8" fill="black"/>
                
                <path d="M 30,10 H 40 V 20 H 30 Z M 45,5 H 55 V 15 H 45 Z M 60,15 H 70 V 25 H 60 Z M 10,30 H 20 V 40 H 10 Z M 35,30 H 45 V 50 H 35 Z M 55,30 H 65 V 45 H 55 Z M 75,35 H 85 V 45 H 75 Z M 20,50 H 30 V 65 H 20 Z M 45,50 H 55 V 60 H 45 Z M 65,55 H 75 V 70 H 65 Z M 35,70 H 45 V 80 H 35 Z M 55,75 H 65 V 90 H 55 Z M 75,75 H 90 V 85 H 75 Z M 80,60 H 90 V 70 H 80 Z" fill="black"/>
            </svg>
        </div>

        <div class="tax-info">
            Informação dos Tributos Totais Incidentes (Lei Federal 12.741/2012):<br>
            Federal: R$ {tributos*0.4:.2f} | Estadual: R$ {tributos*0.6:.2f} (Total: R$ {tributos:.2f})
        </div>

        <div class="footer">
            <strong>OBRIGADO PELA PREFERÊNCIA!</strong><br>
            Desenvolvido por Antigravity AI
        </div>
    </div>
</body>
</html>"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        return jsonify({'success': True, 'url': '/cupom_fiscal'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cupom_fiscal')
def ver_cupom():
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cupom_fiscal.html')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return "Cupom não encontrado", 404

@app.route('/api/produtos/<int:id>', methods=['PUT'])
def update_produto(id):
    try:
        produto_atualizado = request.json
        data = load_data()
        produtos = data.get('produtos', [])
        
        for i, p in enumerate(produtos):
            if p['id'] == id:
                produtos[i].update(produto_atualizado)
                produtos[i]['id'] = id
                data['produtos'] = produtos
                save_data(data)
                return jsonify(produtos[i])
                
        return jsonify({'error': 'Produto não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

SALES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vendas.json')

def load_sales():
    if not os.path.exists(SALES_FILE):
        return []
    with open(SALES_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except:
            return []

def save_sales(sales):
    with open(SALES_FILE, 'w', encoding='utf-8') as f:
        json.dump(sales, f, indent=2, ensure_ascii=False)

@app.route('/api/vendas', methods=['GET'])
def get_vendas():
    try:
        return jsonify(load_sales())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/vendas', methods=['POST'])
def save_venda():
    try:
        venda = request.json
        sales = load_sales()
        venda['id'] = len(sales) + 1
        import datetime
        venda['data'] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        sales.append(venda)
        save_sales(sales)
        return jsonify(venda), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Iniciando Servidor Web na porta 5000...")
    print("Acesse: http://localhost:5000 no seu navegador")
    app.run(debug=True, port=5000)  