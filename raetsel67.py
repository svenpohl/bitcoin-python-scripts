# -*- coding: utf-8 -*-

"""
Rätsel 66 (13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so) wurde am 12.09.2024 geknackt (siehe https://privatekeys.pw/puzzles/bitcoin-puzzle-tx)
Dieses Skript beginnt mit Rätsel 66


Beispiel:
 aus
 0000000000000000000000000000000000000000000000000000000000000007
 wird (uncompressed) zur Adresse
 19ZewH8Kk1PDbSNdJ97FP4EiCjTRaZMZQA
 umgewandelt. Sobald ein PrivateKey zur Zieladresse 1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9 führt,
 stoppt das Script und gibt den WIF (Wallet-Import-Format) aus, den man z.B. in der Elektrum-Wallet 
 importieren kann.
  
Hinweis:
 Für einen zufälligen Startwert in Zeile 70 das "sys.exit(0)" auskommentieren und in eine "start.txt" 
 schreiben!

"""

import os
import sys
import ecdsa
import binascii
import hashlib
import base58
import base64
import logging
import curses
import time
import random

#zieladdress = "19ZewH8Kk1PDbSNdJ97FP4EiCjTRaZMZQA" # Rätsel 3
#zieladdress = "13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so" # Rätsel 66
zieladdress = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9" # Rätsel 67




# Konfiguriere das Logging-Modul
logging.basicConfig(
    filename='mining.log',  # Name der Logdatei
    level=logging.DEBUG,    # Setze das Log-Level auf DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # Format der Lognachricht
)

# Erzeuge Logger-Objekt
logger = logging.getLogger(__name__)


   
    
    
def random_hex_in_range():
    # Kleinster und größter Wert im Dezimalformat
    min_val = int('0000000000000000000000000000000000000000000000040000000000000000', 16)
    max_val = int('000000000000000000000000000000000000000000000007ffffffffffffffff', 16)

    # Zufällige Zahl zwischen min_val und max_val generieren
    random_val = random.randint(min_val, max_val)

    # Zufälligen Wert in einen 32-Byte-Hex-String umwandeln
    random_hex = format(random_val, '064x')
    return random_hex

# Beispielhafter Aufruf (für einen zufälligen Startwert)
val = random_hex_in_range()
print("Random Key: ")
print( val )
#sys.exit(0) 



 
def increment_byte_array(var):
    carry = 1  						# Startet mit einem Übertrag von 1 (der Inkrementierung)
    for i in range(31, -1, -1):  	# Durchläuft das Array von hinten nach vorne
        if carry == 0:
            break
        new_value = var[i] + carry
        var[i] = new_value % 256  	# Modulo 256, um Überlauf zu handhaben
        carry = new_value // 256  	# Berechne den neuen Übertrag
    return var

 



 
#------------------------------
def getaddress( private_key ):
	 
	extended_key = "80"+private_key
	first_sha256 = hashlib.sha256(binascii.unhexlify(extended_key)).hexdigest()
	second_sha256 = hashlib.sha256(binascii.unhexlify(first_sha256)).hexdigest()

	# add checksum to end of extended key
	final_key = extended_key+second_sha256[:8]

    # Wallet Import Format = base 58 encoded final_key
	WIF = base58.b58encode(binascii.unhexlify(final_key))

	PRIVATE = WIF;


	Private_key = binascii.unhexlify(private_key)

	signing_key = ecdsa.SigningKey.from_string(Private_key, curve = ecdsa.SECP256k1)
	verifying_key = signing_key.get_verifying_key()
	public_key = binascii.unhexlify("04") + verifying_key.to_string()

	public_key2 = binascii.hexlify( public_key );




	pubkey = ( public_key2 );
	

    # See 'compressed form' at https://en.bitcoin.it/wiki/Protocol_documentation#Signatures
    #	compress_pubkey = False
	compress_pubkey = True



	def hash160(hex_str):
	    sha = hashlib.sha256()
	    rip = hashlib.new('ripemd160')
	    sha.update(hex_str)
	    rip.update( sha.digest() )
	    #print ( "key_hash = \t" + rip.hexdigest() )
	    return rip.hexdigest()  # .hexdigest() is hex ASCII


	if (compress_pubkey):
	    if (ord(bytearray.fromhex(pubkey[-2:].decode('utf-8'))) % 2 == 0):   # neu
	        pubkey_compressed = '02'
	    else:
	        pubkey_compressed = '03'
	    pubkey_compressed += pubkey[2:66].decode('utf-8') # neu
	    hex_str = bytearray.fromhex(pubkey_compressed)
	else:
	    hex_str = bytearray.fromhex(pubkey)

    # Obtain key:

	key_hash = '00' + hash160(hex_str)

    # Obtain signature:
	sha = hashlib.sha256()
	sha.update( bytearray.fromhex(key_hash) )
	checksum = sha.digest()
	sha = hashlib.sha256()
	sha.update(checksum)
	checksum = sha.hexdigest()[0:8]


	PUBLIC = base58.b58encode( bytes(bytearray.fromhex(key_hash + checksum))   )
 
	PUBLIC2 = PUBLIC.decode('utf-8')

	 
	return PUBLIC2
#------------------------------ getaddress



#------------------------------
def getwif( private_key ):
	 
	extended_key = "80"+private_key
	first_sha256 = hashlib.sha256(binascii.unhexlify(extended_key)).hexdigest()
	second_sha256 = hashlib.sha256(binascii.unhexlify(first_sha256)).hexdigest()

	# add checksum to end of extended key
	final_key = extended_key+second_sha256[:8]

	# Wallet Import Format = base 58 encoded final_key
	WIF = base58.b58encode(binascii.unhexlify(final_key))

	return WIF;
# ----	getwif




stdscr = curses.initscr()  # Initialisiere das Terminal
curses.curs_set(1)         # Verstecke den Cursor
stdscr.nodelay(1)          # Setze den non-blocking Modus für getch

stdscr.addstr("Drücke eine Taste, um das Programm zu beenden.")
#stdscr.refresh() 

 
 

 



# Schritt 2: Lese den Inhalt der Datei wieder ein
with open('start.txt', 'r') as file:
    content = file.read()
    trimmed_content = content.strip()    
hexstr = trimmed_content

#hexstr = "0000000000000000000000000000000000000000000000000000000000000000" # Testen Rätsel 3
#hexstr = "000000000000000000000000000000000000000000000002832ed74f2b5e35ea" # testen Rätsel 66   

bytearray2 = binascii.unhexlify(hexstr)
bytearray3 = bytes(bytearray2)

 


 
	 

 
# Umwandlung in ein bytearray-Objekt
var = bytearray(bytearray3)



aktiv = 1
i     = 0
wif   = ""
wif2  = ""

while aktiv == 1:
    time.sleep(0.01) # Damit der Lüfter nicht anspringt, künstliche Pause
    sys.stdout.flush()
    stdscr.clear() 
    
    
    
    
    # 1) Keygenerierung durch Incrementierung
    increment_byte_array(var)

    private_key = binascii.hexlify( var ).decode()
    print("private key 1 = " + private_key + " " )
    print(i)

    newaddress = getaddress(  private_key )   

    if newaddress == zieladdress:
        print("GEFUNDEN 1!");
        sys.stdout.write("\GEFUNDEN 1!: {i} \n")
        wif = getwif(  private_key )
        print("wif key1 = ")
        print( wif )
        aktiv = 0

    i += 1
    
    
    
    
    # 2) Keygenerierung durch zufälligen Wert aus dem Wertebereich nehmen
    # auf "if 1:" setzen für aktivierung
#    if 1:
    if 0:
        var2 = random_hex_in_range()
        
        #private_key2 = binascii.hexlify( var2 ).decode()
        private_key2 = var2
        print("private key 2 = " + private_key2 + " " )
    
        newaddress2 = getaddress(  private_key2 )   

        if newaddress2 == zieladdress:
            print("GEFUNDEN 2!");
            sys.stdout.write("\GEFUNDEN 2!: {i} \n")
            wif2 = getwif(  private_key2 )
            print("wif key2 = ")
            print( wif2 )
            aktiv = 0
    
        
          
    #
    
            
    key = stdscr.getch()   # Warte auf eine Tasteneingabe
         
    if key != -1:
         print("Taste '#' wurde gedrückt. Beende die Schleife.\r\n")
         print("private key  = " + private_key + "\n")
         print("wif key2 = " + "\n")
         print( wif )
         print("\n");
         aktiv = 0    

    
     

print("Gefundener private key1 = " + private_key + "\n")
print("newaddress = " + newaddress + "\n")
print("wif key = ", wif , "\n")

print("Gefundener private key2 = " + private_key2 + "\n")
print("newaddress2 = " + newaddress2 + "\n")
print("wif key2 = ", wif2 , "\n")
print("\n")
print("i: " , i , "\n")

print("\n")


# Bei Unterbrechung letzten Wert in Datei schreiben:
with open('start.txt', 'w') as file:
    file.write(private_key)

print("\nFIN...")


 


