import camelot as cam
import streamlit as st
import tempfile

def extract_tables_from_pdf(pdf_file, page_range, flavor="stream", edge_tol=500, row_tol=10):
    """Extrait les tables d'un PDF donné à partir d'un ensemble de pages spécifiées."""
    try:
        # Utilisation de Camelot avec des paramètres ajustés
        tables = cam.read_pdf(pdf_file, pages=page_range, flavor=flavor, edge_tol=edge_tol, row_tol=row_tol)
        if tables.n == 0:
            st.write("Aucune table trouvée dans le fichier PDF.")
        return tables
    except Exception as e:
        st.write(f"Erreur lors de l'extraction des tables : {e}")
        return None

def display_extracted_tables(tables):
    """Affiche les tables extraites sous forme de DataFrame et sauvegarde en CSV."""
    if tables and tables.n > 0:
        st.write(f"Nombre de tables trouvées : {tables.n}")
        for i, table in enumerate(tables):
            st.write(f"Table {i + 1}:")
            st.dataframe(table.df)  # Display the table in Streamlit
            # Sauvegarde de la table sous forme de CSV
            csv_file_name = f"table_{i + 1}.csv"
            table.df.to_csv(csv_file_name, index=False)
            st.write(f"Table {i + 1} sauvegardée sous {csv_file_name}")
    else:
        st.write("Aucune table à afficher.")

# Streamlit app starts here
st.title("PDF Table Extraction (Stream Flavor with Enhanced Detection)")

# File uploader for the PDF file
uploaded_pdf = st.file_uploader("Téléverser un fichier PDF", type=["pdf"])

if uploaded_pdf is not None:
    # Save the uploaded PDF in a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(uploaded_pdf.read())
        temp_pdf_path = temp_pdf.name

    # Ask for the page range to extract tables from
    page_range = st.text_input("Entrez la plage de pages pour extraire les tables (ex: 1-5, 3)", "1")

    if st.button("Extraire les tables"):
        # Extract tables from the specified page range
        tables = extract_tables_from_pdf(temp_pdf_path, page_range, flavor="stream", edge_tol=500, row_tol=10)

        # Display the extracted tables
        display_extracted_tables(tables)
else:
    st.write("Veuillez téléverser un fichier PDF pour extraire les tables.")
