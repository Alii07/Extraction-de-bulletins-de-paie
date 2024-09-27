import subprocess
import os
import base64
import camelot as cam

def install_ghostscript():
    """Installe Ghostscript sur la machine si nécessaire."""
    try:
        # Vérifie si Ghostscript est déjà installé
        subprocess.check_call(['gs', '--version'])
        print("Ghostscript est déjà installé.")
    except subprocess.CalledProcessError:
        # Si Ghostscript n'est pas installé, essaie de l'installer
        print("Installation de Ghostscript...")
        proc = subprocess.Popen('apt-get install -y ghostscript', shell=True, stdin=None, stdout=open(os.devnull, "wb"), stderr=subprocess.STDOUT, executable="/bin/bash")
        proc.wait()

def save_pdf(input_pdf_content, output_file):
    """Enregistre un contenu de PDF (sous forme de bytes) en fichier PDF."""
    with open(output_file, "wb") as f:
        base64_pdf = base64.b64encode(input_pdf_content).decode('utf-8')
        f.write(base64.b64decode(base64_pdf))

def extract_tables_from_pdf(pdf_file, page_number):
    """Extrait les tables d'un PDF donné à partir d'une page spécifiée."""
    try:
        # Utilisation de Camelot pour extraire les tables
        tables = cam.read_pdf(pdf_file, pages=str(page_number), flavor='stream')
        if tables.n == 0:
            print("Aucune table trouvée dans le fichier PDF.")
        return tables
    except Exception as e:
        print(f"Erreur lors de l'extraction des tables : {e}")
        return None

def display_extracted_tables(tables):
    """Affiche les tables extraites sous forme de DataFrame et sauvegarde en CSV."""
    if tables and tables.n > 0:
        print(f"Nombre de tables trouvées : {tables.n}")
        for i, table in enumerate(tables):
            print(f"Table {i + 1}:")
            print(table.df)
            # Sauvegarde de la table sous forme de CSV
            csv_file_name = f"table_{i + 1}.csv"
            table.df.to_csv(csv_file_name, index=False)
            print(f"Table {i + 1} sauvegardée sous {csv_file_name}")
    else:
        print("Aucune table à afficher.")

# Fonction principale
if __name__ == "__main__":
    # Installer Ghostscript si nécessaire
    install_ghostscript()

    # Nom du fichier PDF à traiter
    input_pdf_path = "input.pdf"

    # Simuler l'entrée d'un fichier PDF (byte object)
    # En supposant que le fichier PDF ait été déjà lu et encodé
    pdf_byte_content = open(input_pdf_path, "rb").read()

    # Sauvegarder le fichier PDF localement
    save_pdf(pdf_byte_content, "input_saved.pdf")

    # Spécifiez le numéro de page à extraire
    page_number = input("Entrez le numéro de la page à partir de laquelle extraire les tables (ex: 3) : ")

    # Extraire les tables du PDF
    tables = extract_tables_from_pdf("input_saved.pdf", page_number)

    # Afficher les tables extraites et les sauvegarder
    display_extracted_tables(tables)
