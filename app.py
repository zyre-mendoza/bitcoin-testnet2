from flask import Flask, render_template, request,jsonify
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI

app = Flask(__name__)

# Define your Bitcoin Testnet code as a function
def send_bitcoin(sender_private_key, recipient_address, amount_to_send):
    sender_key = PrivateKeyTestnet(sender_private_key)
    
    # Calculate tax amounts
    philhealth_tax = 0.06 * amount_to_send
    pagibig_tax = 0.05 * amount_to_send
    sss_tax = 0.04 * amount_to_send
    
    # Deduct taxes from the total amount
    total_deductions = philhealth_tax + pagibig_tax + sss_tax
    amount_after_deductions = amount_to_send - total_deductions
    
    # Create the transaction
    tx_hex = sender_key.create_transaction(outputs=[(recipient_address, amount_after_deductions, 'btc')])
    signed_tx_hex = sender_key.sign_transaction(tx_hex)
    tx_id = NetworkAPI.broadcast_tx_testnet(signed_tx_hex)
    
    # Return transaction ID and deducted tax amounts
    return tx_id, {
        'philhealth_tax': philhealth_tax,
        'pagibig_tax': pagibig_tax,
        'sss_tax': sss_tax,
    }


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sender_private_key = request.form['sender_private_key']
        recipient_address = request.form['recipient_address']
        amount_to_send = float(request.form['amount_to_send'])
        
        tx_id, tax_deductions = send_bitcoin(sender_private_key, recipient_address, amount_to_send)
        
        return render_template('result.html', tx_id=tx_id, tax_deductions=tax_deductions)
    
    return render_template('index.html')



@app.route('/check_balance', methods=['POST'])
def check_balance():
    sender_private_key = request.form['sender_private_key']

    try:
        # Create a PrivateKeyTestnet instance
        sender_key = PrivateKeyTestnet(sender_private_key)

        # Get the balance
        balance = sender_key.get_balance('btc')

        return render_template('index.html', balance=balance)
    except Exception as e:
        # Handle any errors that occur during balance retrieval
        return render_template('index.html', error=str(e))



if __name__ == '__main__':
    app.run(debug=True)
