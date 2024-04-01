import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

def readExcel(nomFich,nbrange):
    existing_data = conn.read(worksheet=nomFich, usecols=list(range(nbrange)), ttl=5)
    existing_data = existing_data.dropna(how="all")
    st.markdown(nomFich)       
    
    return existing_data



def trouveId(existing_data):
        if(len(existing_data)>0):
            existing_data=existing_data.sort_values(by='ID', ascending=False)
            id=existing_data["ID"].iloc[0]+1         
        else :  
            id=1
        return id


def verifChamp(*args):
    for arg in args:
        if(not arg):
            return False
            break
    return True


def update(data,data_new,nomFich):
    updated_df_new = pd.concat([data, data_new], ignore_index=True)
    conn.update(worksheet=nomFich, data=updated_df_new)
    return True


def supprime(data,nomFich):
        with st.form(key="Delete"):
            data_to_delete = st.selectbox(
                    "Sélectionnez pour supprimer", options=(data['ID'].astype(str) + ' - '  +data["Date"]+ ' - '  +data["Montant"].astype(str)).tolist()
                    
                )
            
            data_to_delete_id=float(data_to_delete.split(" - ")[0].strip())
            
            delete_button = st.form_submit_button(label="Supprimer")
            if delete_button:
                    
                    data.drop(
                        data[data["ID"] == data_to_delete_id].index,
                        inplace=True,
                    )
                
                    conn.update(worksheet=nomFich, data=data)
                    st.success("Supprimée avec succès !")


def updateForm(data):
        st.markdown("Sélectionnez et mettez à jour.")

        data_to_update = st.selectbox(
                "Sélectionnez", options=(data['ID'].astype(str) + ' - '  +data["Date"]+ ' - '  +data["Montant"].astype(str)).tolist()
            )
        try:
                
                data_to_update_id=float(data_to_update.split(" - ")[0].strip())
        except:
                pass
            
        pre_data = data[data["ID"] == data_to_update_id].iloc[
                0
            ]
        return pre_data


#caisse
st.title("Caisse")

conn = st.connection("gsheets", type=GSheetsConnection)
action = st.selectbox(
    "Choisir une action",
    [
        "Caisse",
        "Encaissement d'argent (+)",
        "Décaissement d'argent (-)",
        
    ],

    
)

if action == "Caisse":   
    dataCiasse=readExcel("Caisse",1)
    st.dataframe(dataCiasse)
if action=="Encaissement d'argent (+)":
    dataEnc=readExcel("Encaissement",6)
    with st.form(key="Ajouter Encaissement"):
        
        idEnc=trouveId(dataEnc)
        date = st.date_input(label="Date*")
        montant = st.text_input(label="Montant*")
        source = st.text_input(label="Source*")
        fact=st.text_input(label="Numéro de facture")
        commentaire=st.text_area(label="Commentaire")
        st.markdown("**required*")
        submit_button = st.form_submit_button(label="Confirmer")
        if submit_button:
            if not(verifChamp(date,montant,source)):
                st.warning("Assurez-vous que tous les champs obligatoires sont remplis.")
                st.stop()
            else :
                data_new = pd.DataFrame(
                    [
                        {
                            "ID":idEnc,
                            "Date": date.strftime("%Y/%m/%d"),
                            "Montant": float(montant),    
                            "Source":source,
                            "Commentaire":commentaire,                  
                            "Numéro de facture":fact                          
                        }
                    ]
                    )
                if update(dataEnc,data_new,"Encaissement"):
                    st.success("Ajoutée avec succès.")
    if(len(dataEnc)>0):
        supprime(dataEnc,"Encaissement")
        pre_data=updateForm(dataEnc)
        with st.form(key="update_form"):
            
            date = st.date_input(label="Date*", value=pd.to_datetime(pre_data["Date"]))
            montant = st.text_input(label="Montant*", value=pre_data["Montant"])
            source = st.text_input(label="Source*", value=pre_data["Source"])
            fact=st.text_input(label="Numéro de facture", value=pre_data["Numéro de facture"])
            commentaire=st.text_area(label="Commentaire", value=pre_data["Commentaire"])
            
            update_button = st.form_submit_button(label="Mettre à jour")
            if update_button:
                if not(verifChamp(date,montant,source)):
                    st.warning("Assurez-vous que tous les champs obligatoires sont remplis.")
                    st.stop()
                else : 
                    existing_data=readExcel("Encaissement",6)
                    existing_data.drop(
                        existing_data[
                            
                            (existing_data["ID"]==pre_data["ID"])
                           
                        ].index,
                        inplace=True,
                    )
                    updated_data = pd.DataFrame(
                        [
                            {
                                "ID":pre_data["ID"],
                                "Date": date.strftime("%Y/%m/%d"),
                                "Montant": float(montant),    
                                "Source":source,
                                "Commentaire":commentaire,
                                "Numéro de facture":fact   
                            }
                        ])
                    
                    if update(existing_data,updated_data,"Encaissement"):
                        st.success("Terminé avec succès.")
    st.dataframe(dataEnc)                     

               
if action=="Décaissement d'argent (-)":
    dataDec=readExcel("Décaissement",5)
    
    with st.form(key="Ajouter Décaissement"):
        
        idEnc=trouveId(dataDec)
        date = st.date_input(label="Date*")
        montant = st.text_input(label="Montant*")
        destination = st.text_input(label="Destination*")
        fact=st.text_input(label="Numéro de facture")
        commentaire=st.text_area(label="Commentaire")
        st.markdown("**required*")
        submit_button = st.form_submit_button(label="Confirmer")
        if submit_button:
            if not(verifChamp(date,montant,destination)):
                st.warning("Assurez-vous que tous les champs obligatoires sont remplis.")
                st.stop()
            else :
                data_new = pd.DataFrame(
                    [
                        {
                            "ID":idEnc,
                            "Date": date.strftime("%Y/%m/%d"),
                            "Montant": float(montant),    
                            "Destination":destination,
                            "Commentaire":commentaire,                  
                            "Numéro de facture":fact       
                        }
                    ]
                    )
                if update(dataDec,data_new,"Décaissement"):
                    st.success("Ajoutée avec succès.")
    if(len(dataDec)>0):
        supprime(dataDec,"Décaissement")
        pre_data=updateForm(dataDec)
        with st.form(key="update_form"):
            
            date = st.date_input(label="Date*", value=pd.to_datetime(pre_data["Date"]))
            montant = st.text_input(label="Montant*", value=pre_data["Montant"])
            destination = st.text_input(label="Destination*", value=pre_data["Destination"])
            fact=st.text_input(label="Numéro de facture", value=pre_data["Numéro de facture"])
            commentaire=st.text_area(label="Commentaire", value=pre_data["Commentaire"])
            
            update_button = st.form_submit_button(label="Mettre à jour")
            if update_button:
                if not(verifChamp(date,montant,destination)):
                    st.warning("Assurez-vous que tous les champs obligatoires sont remplis.")
                    st.stop()
                else : 
                    existing_data=readExcel("Décaissement",5)
                    existing_data.drop(
                        existing_data[
                            
                            (existing_data["ID"]==pre_data["ID"])
                           
                        ].index,
                        inplace=True,
                    )
                    updated_data = pd.DataFrame(
                        [
                            {
                                "ID":pre_data["ID"],
                                "Date": date.strftime("%Y/%m/%d"),
                                "Montant": float(montant),    
                                "Destination":destination,
                                "Commentaire":commentaire,
                                "Numéro de facture":fact   
                            }
                        ])
                    
                    if update(existing_data,updated_data,"Décaissement"):
                        st.success("Terminé avec succès.")
    st.dataframe(dataDec)                     

