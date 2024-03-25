import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Display Title and Description
st.title("Enterprise resource planning")


# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)
action = st.selectbox(
    "Choisir une action",
    [
        "Ajouter Client",
        "Stock",
        "Matiere premiere vendu",
        "Ventes",
        "Fournisseurs",
        "Revenu",
        "Dépenses",
        "Fiche d'argent"
        
    ],
)

# Stock


if action == "Stock":
    with st.form(key="AYD_form"):
        # Fetch existing data
        existing_data = conn.read(worksheet="Stock", usecols=list(range(10)), ttl=5)
        existing_data = existing_data.dropna(how="all")
        st.markdown("Stock")
        if(len(existing_data)>0):
            existing_data=existing_data.sort_values(by='ID', ascending=False)
            
            id=existing_data["ID"].iloc[0]+1
            
        else :
            
            id=1
            
        existing_data_four = conn.read(worksheet="Fournisseurs", usecols=list(range(2)), ttl=5)
        existing_data_four = existing_data_four.dropna(how="all")
        st.markdown("Ajouter une matière première")
        # business_type = st.selectbox("Business Type*", options=BUSINESS_TYPES, index=None)
        # products = st.multiselect("Products Offered", options=PRODUCTS)
        # Couleur = st.slider("Years in Business", 0, 50, 5)
        # # print(existing_data["ID"].tolist())
        
        product_name = st.text_input(label="Nom du produit*")
        
        couleur = st.text_input(label="Couleur du produit*")
        date = st.date_input(label="Date*")
        quantité = st.text_input(label="Quantité*")
        taille = st.text_input(label="Taille")
        prix_unitaire = st.text_input(label="Prix unitaire*")
        prix_total= st.text_input(label="Prix total*")
        fournisseur = st.selectbox("Fournisseur*", options= existing_data_four["Nom du fournisseur"], index=None)
        matricule = st.text_input(label="Numéro de facture*")
        # Mark mandatory fields

        st.markdown("**Obligatoire*")
        
        submit_button = st.form_submit_button(label="Confirmer")
    
        
        # If the submit button is pressed
        if submit_button:
            # Check if all mandatory fields are filled
            if not product_name or not couleur or not date or not quantité or not prix_unitaire or not prix_total or not fournisseur:
                st.warning("Assurez-vous que tous les champs obligatoires sont remplis.")
                st.stop()
            # elif existing_data["CompanyName"].str.contains(company_name).any():
            #     st.warning("A vendor with this company name already exists.")
            #     st.stop()
            else:
                
                # Create a new row of vendor data
                matPre_data = pd.DataFrame(
                    [
                        {
                            "ID":id,
                            "Nom du produit": product_name,
                            "Couleur": couleur,
                            "Date": date.strftime("%Y-%m-%d"),
                            "Quantité": quantité,
                            "Taille":taille,
                            "Prix unitaire": prix_unitaire,
                            "Prix total": prix_total,
                            "Nom du fournisseur": fournisseur,
                            "Numéro de facture":matricule,
                        }
                    ]
                )

                # Add the new vendor data to the existing data
                updated_df = pd.concat([existing_data, matPre_data], ignore_index=True)

                # Update Google Sheets with the new vendor data
                conn.update(worksheet="Stock", data=updated_df)

                
                

                    # --------------------------------
                # depense
                existing_data_dep = conn.read(worksheet="Dépenses", usecols=list(range(6)), ttl=5)
                existing_data_dep= existing_data_dep.dropna(how="all")
                st.markdown("Dépenses")                    
                if(len(existing_data_dep)>0):
                        existing_data_dep=existing_data_dep.sort_values(by='ID', ascending=False)                      
                        id_dep=existing_data_dep["ID"].iloc[0]+1                       
                else :
                        id_dep=1
                dep_data_new = pd.DataFrame(
                    [
                        {
                            "ID":id_dep,
                            "Montant": prix_total,    
                            "Source":fournisseur,                        
                            "Date": date.strftime("%Y-%m-%d"),
                            "Numéro de facture":matricule,                           
                        }
                    ]
                    )
                updated_df_new_rev = pd.concat([existing_data_dep, dep_data_new], ignore_index=True)
                conn.update(worksheet="Dépenses", data=updated_df_new_rev)
                st.success("Ajoutée avec succès.")                  
    if(len(existing_data)>0):
        mat_to_delete = st.selectbox(
                "Sélectionnez une matière première à supprimer", options=(existing_data['ID'].astype(str) + ' - ' +existing_data["Nom du produit"]+ ' - ' +existing_data["Couleur"]+ ' - ' +existing_data["Date"]).tolist()
                # existing_data["ID"].tolist()+existing_data["Nom du produit"].tolist()
            )
        try:
            
            mat_to_delete_id=float(mat_to_delete.split(" - ")[0].strip())
        except:
            pass
        if st.button("Supprimer"):
                
                existing_data.drop(
                    existing_data[existing_data["ID"] == mat_to_delete_id].index,
                    inplace=True,
                )
            
                conn.update(worksheet="Stock", data=existing_data)
                st.success("Supprimée avec succès !")
    
    

    if(len(existing_data)>0):
        st.markdown("Sélectionnez et mettez à jour.")

        mat_to_update = st.selectbox(
                "Sélectionnez une matière première", options=(existing_data['ID'].astype(str) + ' - ' +existing_data["Nom du produit"]+ ' - ' +existing_data["Date"]).tolist()
            )
        try:
                
                mat_to_update_id=float(mat_to_update.split(" - ")[0].strip())
        except:
                pass
            
        pre_data = existing_data[existing_data["ID"] == mat_to_update_id].iloc[
                0
            ]
        with st.form(key="update_form"):
            
            product_name = st.text_input(label="Nom du produit*" , value=pre_data["Nom du produit"])
            couleur = st.text_input(label="Couleur du produit*", value=pre_data["Couleur"])
            date = st.date_input(
                label="Date*", value=pd.to_datetime(pre_data["Date"])
            )
            quantité = st.text_input(label="Quantité*", value=pre_data["Quantité"])
            taille = st.text_input(label="Taille", value=pre_data["Taille"])
            prix_unitaire = st.text_input(label="Prix unitaire*", value=pre_data["Prix unitaire"])
            prix_total= st.text_input(label="Prix total*",value=pre_data["Prix total"])
            matricule = st.text_input(label="Numéro de facture*",value=pre_data["Numéro de facture"])
            try :
                fournisseur = st.selectbox("Fournisseur*", options=existing_data_four["Nom du fournisseur"], index=(existing_data_four["Nom du fournisseur"].tolist()).index(pre_data["Nom du fournisseur"]))
            except :
                # print("--------------------------------------")
                # print(pre_data)
                fournisseur =st.text_input(label="Fournisseur*", value=pre_data["Nom du fournisseur"])

            st.markdown("**required*")
            update_button = st.form_submit_button(label="Mettre à jour les détails sur le fournisseur")

            if update_button:
                if not product_name or not couleur or not date or not quantité or not prix_unitaire or not prix_total or not fournisseur:
                    st.warning("Assurez-vous que tous les champs obligatoires sont remplis.")
                else:
                    existing_data_dep = conn.read(worksheet="Dépenses", usecols=list(range(15)), ttl=5)
                    existing_data_dep= existing_data_dep.dropna(how="all")
                    existing_data_dep.drop(
                        existing_data_dep[
                            (existing_data_dep["Nom du produit"] == product_name)& 
                            (existing_data_dep["Date"]==date)&
                            (existing_data_dep["Source"]==fournisseur)
                        ].index,
                        inplace=True,
                    )
                    if(len(existing_data_dep)>0):
                        existing_data_dep=existing_data_dep.sort_values(by='ID', ascending=False)                      
                        id_dep=existing_data_dep["ID"].iloc[0]+1                       
                    else :
                        id_dep=1
                    updated_pre_dep_data = pd.DataFrame(
                        [
                            {
                               "ID":id_dep,
                                "Montant": prix_total,    
                                "Source":fournisseur,                        
                                "Date": date.strftime("%Y-%m-%d"),
                                "Numéro de facture":matricule,  
                            }
                        ]
                    )
                    # Adding updated data to the dataframe
                    updated_df = pd.concat(
                        [existing_data, updated_pre_dep_data], ignore_index=True
                    )
                    conn.update(worksheet="Dépenses", data=updated_df)





                    # Removing old entry
                    existing_data.drop(
                        existing_data[
                            existing_data["ID"] == mat_to_update_id
                        ].index,
                        inplace=True,
                    )
                    # Creating updated data entry
                    updated_pre_data = pd.DataFrame(
                        [
                            {
                                "ID":mat_to_update_id,
                                "Nom du produit": product_name,
                                "Couleur": couleur,
                                "Date": date.strftime("%Y-%m-%d"),
                                "Quantité": quantité,
                                "Taille":taille,
                                "Prix unitaire": prix_unitaire,
                                "Prix total": prix_total,
                                "Nom du fournisseur": fournisseur,
                                "Numéro de facture":matricule,
                            }
                        ]
                    )
                    # Adding updated data to the dataframe
                    updated_df = pd.concat(
                        [existing_data, updated_pre_data], ignore_index=True
                    )
                    conn.update(worksheet="Stock", data=updated_df)
                    st.success("Mise à jour avec succès !")
    st.dataframe(existing_data)


# Matiere premiere vendu
                

elif action == "Matiere premiere vendu":
    existing_data = conn.read(worksheet="Matiere premiere vendu", usecols=list(range(5)), ttl=5)
    existing_data = existing_data.dropna(how="all")
    st.markdown("Matiere premiere vendu")
    st.dataframe(existing_data)
    


# Ventes
    

elif action == "Ventes":
    # with st.form(key="AYD_form"):
    #     STATUS = [
    #         "En attente",
    #         "En cours",
    #         "Terminé",
    #         "Annulé",
    #         "Retour",
            
    #     ]
    #     # Fetch existing data
    #     existing_data = conn.read(worksheet="Ventes", usecols=list(range(17)), ttl=5)
    #     existing_data = existing_data.dropna(how="all")
    #     st.markdown("Ventes")
        
    #     if(len(existing_data)>0):
    #         existing_data=existing_data.sort_values(by='ID Vente', ascending=False)
    #         # st.dataframe(existing_data)
    #         id=existing_data["ID Vente"].iloc[0]+1
    #         # print("new id : ",id)
    #     else :
    #         # st.dataframe(existing_data)
    #         id=1
    #         # print("new id : ",id)
    
    #     st.markdown("Ajouter une vente")
       
        
    #     product_name = st.text_input(label="Nom du produit fini*")
    #     date = st.date_input(label="Date*")
    #     # prix= st.text_input(label="Prix*")
    #     status= st.selectbox("Status*", options=STATUS, index=None)





    #     existing_data_mat = conn.read(worksheet="Stock", usecols=list(range(5)), ttl=5)
    #     existing_data_mat =  existing_data_mat.dropna(how="all")
    #     # # print("...........hhhhhhhhhhhhhhhhhhhh",existing_data_mat)
    #     # # print("------------------------------------------")
    #     #  = st.text_input(label="Quantité 1*")

    #     mat_pre_1 = st.selectbox(
    #         "Matiére premier 1*", options=(existing_data_mat['ID'].astype(str) + ' - '+existing_data_mat["Nom du produit"]+ ' - '+existing_data_mat["Quantité"].astype(str)).tolist()
    #         )
       

    #     quantite_1=  st.text_input(label="Quantité 1*")
    #     if(mat_pre_1!=""):
    #         mat_pre_1_name=mat_pre_1.split(" - ")[1]
    #     else:
    #         mat_pre_1_name=""
    #     mat_pre_2 = st.selectbox(
    #         "Matiére premier 2", options=[""]+(existing_data_mat['ID'].astype(str) + ' - '+existing_data_mat["Nom du produit"]+ ' - '+existing_data_mat["Quantité"].astype(str)).tolist()
    #         )

    #     quantite_2= st.text_input(label="Quantité 2")
    #     if(mat_pre_2!=""):
    #         mat_pre_2_name=mat_pre_2.split(" - ")[1]
    #     else:
    #         mat_pre_2_name=""

      
    #     mat_pre_3 = st.selectbox(
    #         "Matiére premier 3*", options=[""]+(existing_data_mat['ID'].astype(str) + ' - '+existing_data_mat["Nom du produit"]+ ' - '+existing_data_mat["Quantité"].astype(str)).tolist()
    #         )       
    #     quantite_3 = st.text_input(label="Quantité 3")
    #     if(mat_pre_3!=""):
    #         mat_pre_3_name=mat_pre_3.split(" - ")[1]
    #     else:
    #         mat_pre_3_name=""



    #     mat_pre_4 = st.selectbox(
    #         "Matiére premier 4*", options=[""]+(existing_data_mat['ID'].astype(str) + ' - '+existing_data_mat["Nom du produit"]+ ' - '+existing_data_mat["Quantité"].astype(str)).tolist()
    #         )
    #     quantite_4 = st.text_input(label="Quantité 4")
    #     if(mat_pre_4!=""):
    #         mat_pre_4_name=mat_pre_4.split(" - ")[1]

    #     else:
    #         mat_pre_4_name=""


    #     mat_pre_5 = st.selectbox(
    #         "Matiére premier 5", options=[""]+(existing_data_mat['ID'].astype(str) + ' - '+existing_data_mat["Nom du produit"]+ ' - '+existing_data_mat["Quantité"].astype(str)).tolist()
    #         )
    #     quantite_5 = st.text_input(label="Quantité 5")
    #     if(mat_pre_5!=""):
    #         mat_pre_5_name=mat_pre_5.split(" - ")[1]
    #     else:
    #         mat_pre_5_name=""


    #     mat_pre_6 = st.selectbox(
    #         "Matiére premier 6", options=[""]+(existing_data_mat['ID'].astype(str) + ' - '+existing_data_mat["Nom du produit"]+ ' - '+existing_data_mat["Quantité"].astype(str)).tolist()
    #         )
    #     quantite_6 = st.text_input(label="Quantité 6")
    #     if(mat_pre_6!=""):
    #         mat_pre_6_name=mat_pre_6.split(" - ")[1]
    #     else:
    #         mat_pre_6_name=""
        
    #     # Mark mandatory fields
    #     st.markdown("**Obligatoire*")
        
    #     submit_button = st.form_submit_button(label="Confirmer")
    
        
    #     # If the submit button is pressed
    #     if submit_button:
    #         # Check if all mandatory fields are filled
    #         if not product_name or not date or not status or not prix or not mat_pre_1 or not quantite_1 :
    #             st.warning("Assurez-vous que tous les champs obligatoires sont remplis.")
    #             st.stop()
           
    #         else:
    #             # Create a new row of vendor data
    #             ven_data = pd.DataFrame(
    #                 [
    #                     {
    #                         "ID Vente":id,
    #                         "Nom du produit fini": product_name,
                            
    #                         "Date": date.strftime("%Y-%m-%d"),
    #                         "Prix": prix,
    #                         "Status":status,
    #                         "Matiere premiere 1": mat_pre_1_name,
    #                         "Quantité 1":quantite_1,
                            
    #                         "Matiere premiere 2": mat_pre_2_name,
    #                         "Quantité 2":quantite_2,

                        

    #                         "Matiere premiere 3": mat_pre_3_name,
    #                         "Quantité 3":quantite_3,

    #                         "Matiere premiere 4": mat_pre_4_name,
    #                         "Quantité 4":quantite_4,

    #                         "Matiere premiere 5": mat_pre_5_name,
    #                         "Quantité 5":quantite_5,

    #                         "Matiere premiere 6": mat_pre_6_name,
    #                         "Quantité 6":quantite_6,

                            
    #                     }
    #                 ]
    #             )
    #             # table matiere premier vendu
    #             ven_data_pre_1 = pd.DataFrame(
    #                 [
    #                     {
    #                         "ID Vente":id,
    #                         "Nom du matiere": mat_pre_1_name,
                            
    #                         "Date": date.strftime("%Y-%m-%d"),
                            
                            
    #                         "Quantité":quantite_1,
                           
    #                     }
    #                 ]
    #             )
    #             existing_data_mat_ven = conn.read(worksheet="Matiere premiere vendu", usecols=list(range(4)), ttl=5)
    #             existing_data_mat_ven = existing_data_mat_ven.dropna(how="all")    

    #             updated_df_pre_ven = pd.concat([existing_data_mat_ven, ven_data_pre_1], ignore_index=True)

               

    #             if(mat_pre_2!=""):
    #                 ven_data_pre_2 = pd.DataFrame(
    #                 [
    #                     {
    #                         "ID Vente":id,
    #                         "Nom du matiere": mat_pre_2_name,
                            
    #                         "Date": date.strftime("%Y-%m-%d"),
                            
                            
    #                         "Quantité":quantite_2,
                           
    #                     }
    #                 ]
    #                 )
    #                 updated_df_pre_ven = pd.concat([ updated_df_pre_ven, ven_data_pre_2], ignore_index=True)

               
    #             if(mat_pre_3!=""):
    #                 ven_data_pre_3 = pd.DataFrame(
    #                 [
    #                     {
    #                         "ID Vente":id,
    #                         "Nom du matiere": mat_pre_3_name,
                            
    #                         "Date": date.strftime("%Y-%m-%d"),
                            
                            
    #                         "Quantité":quantite_3,
                           
    #                     }
    #                 ]
    #                 )
    #                 updated_df_pre_ven = pd.concat([ updated_df_pre_ven, ven_data_pre_3], ignore_index=True)

    #             if(mat_pre_4!=""):
    #                 ven_data_pre_4 = pd.DataFrame(
    #                 [
    #                     {
    #                         "ID Vente":id,
    #                         "Nom du matiere": mat_pre_4_name,
                            
    #                         "Date": date.strftime("%Y-%m-%d"),
                            
                            
    #                         "Quantité":quantite_4,
                           
    #                     }
    #                 ]
    #                 )
    #                 updated_df_pre_ven = pd.concat([ updated_df_pre_ven, ven_data_pre_4], ignore_index=True)

    #             if(mat_pre_5!=""):
    #                 ven_data_pre_5 = pd.DataFrame(
    #                 [
    #                     {
    #                         "ID Vente":id,
    #                         "Nom du matiere": mat_pre_5_name,
                            
    #                         "Date": date.strftime("%Y-%m-%d"),
                            
                            
    #                         "Quantité":quantite_5,
                           
    #                     }
    #                 ]
    #                 )
    #                 updated_df_pre_ven = pd.concat([ updated_df_pre_ven, ven_data_pre_5], ignore_index=True)

    #             if(mat_pre_6!=""):
    #                 ven_data_pre_6 = pd.DataFrame(
    #                 [
    #                     {
    #                         "ID Vente":id,
    #                         "Nom du matiere": mat_pre_6_name,
                            
    #                         "Date": date.strftime("%Y-%m-%d"),
                            
                            
    #                         "Quantité":quantite_6,
                           
    #                     }
    #                 ]
    #                 )
    #                 updated_df_pre_ven = pd.concat([ updated_df_pre_ven, ven_data_pre_6], ignore_index=True)

    #             conn.update(worksheet="Matiere premiere vendu", data=updated_df_pre_ven)    
                    
    #             # na9sou mil quantité mta3 matiere premiere 
    #             existing_data_mat_exist = conn.read(worksheet="Stock", usecols=list(range(8)), ttl=5)
    #             existing_data_mat_exist = existing_data_mat_exist.dropna(how="all")
    #             try:
                
    #                 mat_1_to_update_id=float(mat_pre_1.split(" - ")[0].strip())
    #             except:
    #                 mat_1_to_update_id=""
    #                 pass
    #             pre_data_1 = existing_data_mat_exist[existing_data_mat_exist["ID"] == mat_1_to_update_id].iloc[
    #             0
    #             ]
    #             # print("--------------pre_data_1[Quantité]------------\n",type(pre_data_1["Quantité"]),"\n--------quantite_1------------\n",type(quantite_1),"\n-----------")
                
    #             if(mat_1_to_update_id!=""):
    #                 existing_data_mat_exist.drop(
    #                     existing_data_mat_exist[
    #                         existing_data_mat_exist["ID"] == mat_1_to_update_id
    #                     ].index,
    #                     inplace=True,
    #                 )
    #                 # Creating updated data entry
    #                 new_pre_1_data = pd.DataFrame(
    #                     [
    #                         {
    #                             "ID":mat_1_to_update_id,
    #                             "Nom du produit": pre_data_1["Nom du produit"],
    #                             "Couleur": pre_data_1["Couleur"],
    #                             "Date": pre_data_1["Date"],
    #                             "Quantité": float(pre_data_1["Quantité"])-float(quantite_1),
    #                             "Prix unitaire": pre_data_1["Prix unitaire"],
    #                             "Prix total": pre_data_1["Prix total"],
    #                             "Nom du fournisseur": pre_data_1["Nom du fournisseur"],
    #                         }
    #                     ]
    #                 )
    #                 updated_df = pd.concat(
    #                         [existing_data_mat_exist, new_pre_1_data], ignore_index=True
    #                     )
    #                 conn.update(worksheet="Stock", data=updated_df)    
                    
    #                 # matiere premiere 2
    #                 if(mat_pre_2!=""):
    #                     try:
                    
    #                         mat_2_to_update_id=float(mat_pre_2.split(" - ")[0].strip())
    #                     except:
    #                         mat_2_to_update_id=""
    #                         pass
    #                     # print("--------updated_df[ID]---------- :  ",updated_df["ID"],"\n-----------------mat_2_to_update_id------------------ : ",mat_2_to_update_id)
    #                     pre_data_2 = updated_df[updated_df["ID"] == mat_2_to_update_id].iloc[
    #                     0
    #                     ]
    #                     # print("--------------pre_data_2[Quantité]------------\n",type(pre_data_2["Quantité"]),"\n--------quantite_2------------\n",type(quantite_2),"\n-----------")
                        
    #                     if(mat_2_to_update_id!=""):
    #                         updated_df.drop(
    #                             updated_df[
    #                                 updated_df["ID"] == mat_2_to_update_id
    #                             ].index,
    #                             inplace=True,
    #                         )
    #                         # Creating updated data entry
    #                         new_pre_2_data = pd.DataFrame(
    #                             [
    #                                 {
    #                                     "ID":mat_2_to_update_id,
    #                                     "Nom du produit": pre_data_2["Nom du produit"],
    #                                     "Couleur": pre_data_2["Couleur"],
    #                                     "Date": pre_data_2["Date"],
    #                                     "Quantité": float(pre_data_2["Quantité"])-float(quantite_2),
    #                                     "Prix unitaire": pre_data_2["Prix unitaire"],
    #                                     "Prix total": pre_data_2["Prix total"],
    #                                     "Nom du fournisseur": pre_data_2["Nom du fournisseur"],
    #                                 }
    #                             ]
    #                         )
    #                         updated_df = pd.concat(
    #                                 [updated_df, new_pre_2_data], ignore_index=True
    #                             )
    #                         conn.update(worksheet="Stock", data=updated_df)    

    #                 if(mat_pre_3!=""):
    #                     try:
                    
    #                         mat_3_to_update_id=float(mat_pre_3.split(" - ")[0].strip())
    #                     except:
    #                         mat_3_to_update_id=""
    #                         pass
    #                     # print("--------updated_df[ID]---------- :  ",updated_df["ID"],"\n-----------------mat_3_to_update_id------------------ : ",mat_3_to_update_id)
    #                     pre_data_3 = updated_df[updated_df["ID"] == mat_3_to_update_id].iloc[
    #                     0
    #                     ]
    #                     # print("--------------pre_data_3[Quantité]------------\n",type(pre_data_3["Quantité"]),"\n--------quantite_3------------\n",type(quantite_3),"\n-----------")
                        
    #                     if(mat_3_to_update_id!=""):
    #                         updated_df.drop(
    #                             updated_df[
    #                                 updated_df["ID"] == mat_3_to_update_id
    #                             ].index,
    #                             inplace=True,
    #                         )
    #                         # Creating updated data entry
    #                         new_pre_3_data = pd.DataFrame(
    #                             [
    #                                 {
    #                                     "ID":mat_3_to_update_id,
    #                                     "Nom du produit": pre_data_3["Nom du produit"],
    #                                     "Couleur": pre_data_3["Couleur"],
    #                                     "Date": pre_data_3["Date"],
    #                                     "Quantité": float(pre_data_3["Quantité"])-float(quantite_3),
    #                                     "Prix unitaire": pre_data_3["Prix unitaire"],
    #                                     "Prix total": pre_data_3["Prix total"],
    #                                     "Nom du fournisseur": pre_data_3["Nom du fournisseur"],
    #                                 }
    #                             ]
    #                         )
    #                         updated_df = pd.concat(
    #                                 [updated_df, new_pre_3_data], ignore_index=True
    #                             )
    #                         conn.update(worksheet="Stock", data=updated_df)    
    #                 if(mat_pre_4!=""):
    #                     try:
                    
    #                         mat_4_to_update_id=float(mat_pre_4.split(" - ")[0].strip())
    #                     except:
    #                         mat_4_to_update_id=""
    #                         pass
    #                     # print("--------updated_df[ID]---------- :  ",updated_df["ID"],"\n-----------------mat_4_to_update_id------------------ : ",mat_4_to_update_id)
    #                     pre_data_4 = updated_df[updated_df["ID"] == mat_4_to_update_id].iloc[
    #                     0
    #                     ]
    #                     # print("--------------pre_data_4[Quantité]------------\n",type(pre_data_4["Quantité"]),"\n--------quantite_4------------\n",type(quantite_4),"\n-----------")
                        
    #                     if(mat_4_to_update_id!=""):
    #                         updated_df.drop(
    #                             updated_df[
    #                                 updated_df["ID"] == mat_4_to_update_id
    #                             ].index,
    #                             inplace=True,
    #                         )
    #                         # Creating updated data entry
    #                         new_pre_4_data = pd.DataFrame(
    #                             [
    #                                 {
    #                                     "ID":mat_4_to_update_id,
    #                                     "Nom du produit": pre_data_4["Nom du produit"],
    #                                     "Couleur": pre_data_4["Couleur"],
    #                                     "Date": pre_data_4["Date"],
    #                                     "Quantité": float(pre_data_4["Quantité"])-float(quantite_4),
    #                                     "Prix unitaire": pre_data_4["Prix unitaire"],
    #                                     "Prix total": pre_data_4["Prix total"],
    #                                     "Nom du fournisseur": pre_data_4["Nom du fournisseur"],
    #                                 }
    #                             ]
    #                         )
    #                         updated_df = pd.concat(
    #                                 [updated_df, new_pre_4_data], ignore_index=True
    #                             )
    #                         conn.update(worksheet="Stock", data=updated_df)    
    #                 if(mat_pre_5!=""):
    #                     try:
                    
    #                         mat_5_to_update_id=float(mat_pre_5.split(" - ")[0].strip())
    #                     except:
    #                         mat_5_to_update_id=""
    #                         pass
    #                     # print("--------updated_df[ID]---------- :  ",updated_df["ID"],"\n-----------------mat_5_to_update_id------------------ : ",mat_5_to_update_id)
    #                     pre_data_5 = updated_df[updated_df["ID"] == mat_5_to_update_id].iloc[
    #                     0
    #                     ]
    #                     # print("--------------pre_data_5[Quantité]------------\n",type(pre_data_5["Quantité"]),"\n--------quantite_5------------\n",type(quantite_5),"\n-----------")
                        
    #                     if(mat_5_to_update_id!=""):
    #                         updated_df.drop(
    #                             updated_df[
    #                                 updated_df["ID"] == mat_5_to_update_id
    #                             ].index,
    #                             inplace=True,
    #                         )
    #                         # Creating updated data entry
    #                         new_pre_5_data = pd.DataFrame(
    #                             [
    #                                 {
    #                                     "ID":mat_5_to_update_id,
    #                                     "Nom du produit": pre_data_5["Nom du produit"],
    #                                     "Couleur": pre_data_5["Couleur"],
    #                                     "Date": pre_data_5["Date"],
    #                                     "Quantité": float(pre_data_5["Quantité"])-float(quantite_5),
    #                                     "Prix unitaire": pre_data_5["Prix unitaire"],
    #                                     "Prix total": pre_data_5["Prix total"],
    #                                     "Nom du fournisseur": pre_data_5["Nom du fournisseur"],
    #                                 }
    #                             ]
    #                         )
    #                         updated_df = pd.concat(
    #                                 [updated_df, new_pre_5_data], ignore_index=True
    #                             )
    #                         conn.update(worksheet="Stock", data=updated_df)
    #                 if(mat_pre_6!=""):
    #                     try:
                    
    #                         mat_6_to_update_id=float(mat_pre_6.split(" - ")[0].strip())
    #                     except:
    #                         mat_6_to_update_id=""
    #                         pass
    #                     # print("--------updated_df[ID]---------- :  ",updated_df["ID"],"\n-----------------mat_6_to_update_id------------------ : ",mat_6_to_update_id)
    #                     pre_data_6 = updated_df[updated_df["ID"] == mat_6_to_update_id].iloc[
    #                     0
    #                     ]
    #                     # print("--------------pre_data_6[Quantité]------------\n",type(pre_data_6["Quantité"]),"\n--------quantite_6------------\n",type(quantite_6),"\n-----------")
                        
    #                     if(mat_6_to_update_id!=""):
    #                         updated_df.drop(
    #                             updated_df[
    #                                 updated_df["ID"] == mat_6_to_update_id
    #                             ].index,
    #                             inplace=True,
    #                         )
    #                         # Creating updated data entry
    #                         new_pre_6_data = pd.DataFrame(
    #                             [
    #                                 {
    #                                     "ID":mat_6_to_update_id,
    #                                     "Nom du produit": pre_data_6["Nom du produit"],
    #                                     "Couleur": pre_data_6["Couleur"],
    #                                     "Date": pre_data_6["Date"],
    #                                     "Quantité": float(pre_data_6["Quantité"])-float(quantite_6),
    #                                     "Prix unitaire": pre_data_6["Prix unitaire"],
    #                                     "Prix total": pre_data_6["Prix total"],
    #                                     "Nom du fournisseur": pre_data_6["Nom du fournisseur"],
    #                                 }
    #                             ]
    #                         )
    #                         updated_df = pd.concat(
    #                                 [updated_df, new_pre_6_data], ignore_index=True
    #                             )
    #                         conn.update(worksheet="Stock", data=updated_df)
                         





    #             # Add the new vendor data to the existing data
    #             updated_df = pd.concat([existing_data, ven_data], ignore_index=True)

    #             # Update Google Sheets with the new matiere premiere data
    #             conn.update(worksheet="Ventes", data=updated_df)

    #             st.success("Vente ajoutée avec succès.")
    existing_data = conn.read(worksheet="Ventes", usecols=list(range(15)), ttl=5)
    existing_data = existing_data.dropna(how="all")
    st.markdown("Ventes")
        
   
    if(len(existing_data)>0):
        existing_data=existing_data.sort_values(by='ID Vente', ascending=False)
        # st.dataframe(existing_data)
        id=existing_data["ID Vente"].iloc[0]+1
        # # print("new id : ",id)
        # ven_to_delete = st.selectbox(
        #         "Sélectionnez une vente à supprimer", options=(existing_data['ID Vente'].astype(str) + ' - ' +existing_data["Nom du produit fini"]+ ' - ' +existing_data["Date"] ).tolist()
        #         # existing_data["ID"].tolist()+existing_data["Nom du produit"].tolist()
        #     )
        # try:
            
        #     ven_to_delete_id=float(ven_to_delete.split(" - ")[0].strip())
        # except:
        #     pass
        # if st.button("Supprimer"):
                
        #         existing_data.drop(
        #             existing_data[existing_data["ID Vente"] == ven_to_delete_id].index,
        #             inplace=True,
        #         )
                
        #         conn.update(worksheet="Ventes", data=existing_data)
        #         st.success("Vente supprimée avec succès !")




       
        # st.markdown("Sélectionnez une vente et mettez à jour ses coordonnées.")

        ven_to_update = st.selectbox(
                "Sélectionnez une vente", options=(existing_data['ID Vente'].astype(str) + ' - ' +existing_data["Nom du produit fini"]+ ' - ' +existing_data["Date"]).tolist()
            )
        try:
                
            ven_to_update_id=float(ven_to_update.split(" - ")[0].strip())
        except:
            pass
        ven_data = existing_data[existing_data["ID Vente"] == ven_to_update_id].iloc[
                0
            ]
        with st.form(key="update_form"):
            existing_data_mat = conn.read(worksheet="Stock", usecols=list(range(5)), ttl=5)
            existing_data_mat =  existing_data_mat.dropna(how="all")
            product_name = st.text_input(label="Nom du produit fini*", value=ven_data["Nom du produit fini"])
            date = st.date_input(label="Date*", value=pd.to_datetime(ven_data["Date"]))
            
            
            mat_pre_1 = st.selectbox(
            "Matiére premier 1*", options=(existing_data_mat['ID'].astype(str) + ' - '+existing_data_mat["Nom du produit"]+ ' - '+existing_data_mat["Quantité"].astype(str)).tolist()
            )
            quantite_1 = st.text_input(label="Quantité 1*",value=ven_data["Quantité 1"])
            if(mat_pre_1!=""):
                mat_pre_1_name=mat_pre_1.split(" - ")[1]
            else:
                mat_pre_1_name=""
            mat_pre_2 = st.selectbox(
            "Matiére premier 2*", options=[""]+(existing_data_mat['ID'].astype(str) + ' - '+existing_data_mat["Nom du produit"]+ ' - '+existing_data_mat["Quantité"].astype(str)).tolist()
            )
            quantite_2 = st.text_input(label="Quantité 2",value=ven_data["Quantité 2"])
            if(mat_pre_2!=""):
                mat_pre_2_name=mat_pre_2.split(" - ")[1]
            else:
                mat_pre_2_name=""
            mat_pre_3 = st.selectbox(
            "Matiére premier 3*", options=[""]+(existing_data_mat['ID'].astype(str) + ' - '+existing_data_mat["Nom du produit"]+ ' - '+existing_data_mat["Quantité"].astype(str)).tolist()
            )
            quantite_3 = st.text_input(label="Quantité 3",value=ven_data["Quantité 3"])
            if(mat_pre_3!=""):
                mat_pre_3_name=mat_pre_3.split(" - ")[1]
            else:
                mat_pre_3_name=""
            mat_pre_4 = st.selectbox(
            "Matiére premier 4*", options=[""]+(existing_data_mat['ID'].astype(str) + ' - '+existing_data_mat["Nom du produit"]+ ' - '+existing_data_mat["Quantité"].astype(str)).tolist()
            )
            quantite_4 = st.text_input(label="Quantité 4",value=ven_data["Quantité 4"])
            if(mat_pre_4!=""):
                mat_pre_4_name=mat_pre_4.split(" - ")[1]

            else:
                mat_pre_4_name=""

            mat_pre_5 = st.selectbox(
            "Matiére premier 5*", options=[""]+(existing_data_mat['ID'].astype(str) + ' - '+existing_data_mat["Nom du produit"]+ ' - '+existing_data_mat["Quantité"].astype(str)).tolist()
            )
            quantite_5 = st.text_input(label="Quantité 5",value=ven_data["Quantité 5"])
            if(mat_pre_5!=""):
                mat_pre_5_name=mat_pre_5.split(" - ")[1]
            else:
                mat_pre_5_name=""
            mat_pre_6 = st.selectbox(
            "Matiére premier 6*", options=[""]+(existing_data_mat['ID'].astype(str) + ' - '+existing_data_mat["Nom du produit"]+ ' - '+existing_data_mat["Quantité"].astype(str)).tolist()
            )
            quantite_6 = st.text_input(label="Quantité 6",value=ven_data["Quantité 6"])
            if(mat_pre_6!=""):
                mat_pre_6_name=mat_pre_6.split(" - ")[1]
            else:
                mat_pre_6_name=""


            
            st.markdown("**required*")
            update_button = st.form_submit_button(label="Mettre à jour les détails")

            if update_button:
                if not product_name or not date or not mat_pre_1 or not quantite_1 :
                    st.warning("Assurez-vous que tous les champs obligatoires sont remplis.")
                else:
                    # Removing old entry
                    existing_data.drop(
                        existing_data[
                            existing_data["ID Vente"] == ven_to_update_id
                        ].index,
                        inplace=True,
                    )
                    # Creating updated data entry
                    updated_ven_data = pd.DataFrame(
                        [
                            {
                            "ID Vente":ven_to_update_id,
                            "Nom du produit fini": product_name,
                            
                            "Date": date.strftime("%Y-%m-%d"),
                            
                            "Matiere premiere 1": mat_pre_1_name,
                            "Quantité 1":quantite_1,

                            "Matiere premiere 2": mat_pre_2_name,
                            "Quantité 2":quantite_2,

                        

                            "Matiere premiere 3": mat_pre_3_name,
                            "Quantité 3":quantite_3,

                            "Matiere premiere 4": mat_pre_4_name,
                            "Quantité 4":quantite_4,

                            "Matiere premiere 5": mat_pre_5_name,
                            "Quantité 5":quantite_5,

                            "Matiere premiere 6": mat_pre_6_name,
                            "Quantité 6":quantite_6,
                            }
                        ]
                    )
                    # Adding updated data to the dataframe
                    updated_df = pd.concat(
                        [existing_data, updated_ven_data], ignore_index=True
                    )
                    conn.update(worksheet="Ventes", data=updated_df)
            # table matiere premier vendu
                    ven_data_pre_1 = pd.DataFrame(
                    [
                        {
                            "ID Vente":id,
                            "Nom du matiere": mat_pre_1_name,
                            
                            "Date": date.strftime("%Y-%m-%d"),
                            
                            
                            "Quantité":quantite_1,
                           
                        }
                    ]
                )
                existing_data_mat_ven = conn.read(worksheet="Matiere premiere vendu", usecols=list(range(4)), ttl=5)
                existing_data_mat_ven = existing_data_mat_ven.dropna(how="all")    

                updated_df_pre_ven = pd.concat([existing_data_mat_ven, ven_data_pre_1], ignore_index=True)

               

                if(mat_pre_2!=""):
                    ven_data_pre_2 = pd.DataFrame(
                    [
                        {
                            "ID Vente":id,
                            "Nom du matiere": mat_pre_2_name,
                            
                            "Date": date.strftime("%Y-%m-%d"),
                            
                            
                            "Quantité":quantite_2,
                           
                        }
                    ]
                    )
                    updated_df_pre_ven = pd.concat([ updated_df_pre_ven, ven_data_pre_2], ignore_index=True)

               
                if(mat_pre_3!=""):
                    ven_data_pre_3 = pd.DataFrame(
                    [
                        {
                            "ID Vente":id,
                            "Nom du matiere": mat_pre_3_name,
                            
                            "Date": date.strftime("%Y-%m-%d"),
                            
                            
                            "Quantité":quantite_3,
                           
                        }
                    ]
                    )
                    updated_df_pre_ven = pd.concat([ updated_df_pre_ven, ven_data_pre_3], ignore_index=True)

                if(mat_pre_4!=""):
                    ven_data_pre_4 = pd.DataFrame(
                    [
                        {
                            "ID Vente":id,
                            "Nom du matiere": mat_pre_4_name,
                            
                            "Date": date.strftime("%Y-%m-%d"),
                            
                            
                            "Quantité":quantite_4,
                           
                        }
                    ]
                    )
                    updated_df_pre_ven = pd.concat([ updated_df_pre_ven, ven_data_pre_4], ignore_index=True)

                if(mat_pre_5!=""):
                    ven_data_pre_5 = pd.DataFrame(
                    [
                        {
                            "ID Vente":id,
                            "Nom du matiere": mat_pre_5_name,
                            
                            "Date": date.strftime("%Y-%m-%d"),
                            
                            
                            "Quantité":quantite_5,
                           
                        }
                    ]
                    )
                    updated_df_pre_ven = pd.concat([ updated_df_pre_ven, ven_data_pre_5], ignore_index=True)

                if(mat_pre_6!=""):
                    ven_data_pre_6 = pd.DataFrame(
                    [
                        {
                            "ID Vente":id,
                            "Nom du matiere": mat_pre_6_name,
                            
                            "Date": date.strftime("%Y-%m-%d"),
                            
                            
                            "Quantité":quantite_6,
                           
                        }
                    ]
                    )
                    updated_df_pre_ven = pd.concat([ updated_df_pre_ven, ven_data_pre_6], ignore_index=True)

                conn.update(worksheet="Matiere premiere vendu", data=updated_df_pre_ven)    

                
         # na9sou mil quantité mta3 matiere premiere 
                existing_data_mat_exist = conn.read(worksheet="Stock", usecols=list(range(10)), ttl=5)
                existing_data_mat_exist = existing_data_mat_exist.dropna(how="all")
                try:
                
                    mat_1_to_update_id=float(mat_pre_1.split(" - ")[0].strip())
                except:
                    mat_1_to_update_id=""
                    pass
                pre_data_1 = existing_data_mat_exist[existing_data_mat_exist["ID"] == mat_1_to_update_id].iloc[
                0
                ]
                # print("--------------pre_data_1[Quantité]------------\n",type(pre_data_1["Quantité"]),"\n--------quantite_1------------\n",type(quantite_1),"\n-----------")
                # print("------------------------\n",pre_data_1,"\n------------------------")
                if(mat_1_to_update_id!=""):
                    existing_data_mat_exist.drop(
                        existing_data_mat_exist[
                            existing_data_mat_exist["ID"] == mat_1_to_update_id
                        ].index,
                        inplace=True,
                    )
                    # Creating updated data entry
                    new_pre_1_data = pd.DataFrame(
                        [
                            {
                                "ID":mat_1_to_update_id,
                                "Nom du produit": pre_data_1["Nom du produit"],
                                "Couleur": pre_data_1["Couleur"],
                                "Date": pre_data_1["Date"],
                                "Quantité": float(pre_data_1["Quantité"])-float(quantite_1),
                                "Prix unitaire": pre_data_1["Prix unitaire"],
                                "Prix total": pre_data_1["Prix total"],
                                "Nom du fournisseur": pre_data_1["Nom du fournisseur"],
                            }
                        ]
                    )
                    updated_df = pd.concat(
                            [existing_data_mat_exist, new_pre_1_data], ignore_index=True
                        )
                    conn.update(worksheet="Stock", data=updated_df)    
                    
                    # matiere premiere 2
                    if(mat_pre_2!=""):
                        try:
                    
                            mat_2_to_update_id=float(mat_pre_2.split(" - ")[0].strip())
                        except:
                            mat_2_to_update_id=""
                            pass
                        # print("--------updated_df[ID]---------- :  ",updated_df["ID"],"\n-----------------mat_2_to_update_id------------------ : ",mat_2_to_update_id)
                        pre_data_2 = updated_df[updated_df["ID"] == mat_2_to_update_id].iloc[
                        0
                        ]
                        # print("--------------pre_data_2[Quantité]------------\n",type(pre_data_2["Quantité"]),"\n--------quantite_2------------\n",type(quantite_2),"\n-----------")
                        
                        if(mat_2_to_update_id!=""):
                            updated_df.drop(
                                updated_df[
                                    updated_df["ID"] == mat_2_to_update_id
                                ].index,
                                inplace=True,
                            )
                            # Creating updated data entry
                            new_pre_2_data = pd.DataFrame(
                                [
                                    {
                                        "ID":mat_2_to_update_id,
                                        "Nom du produit": pre_data_2["Nom du produit"],
                                        "Couleur": pre_data_2["Couleur"],
                                        "Date": pre_data_2["Date"],
                                        "Quantité": float(pre_data_2["Quantité"])-float(quantite_2),
                                        "Prix unitaire": pre_data_2["Prix unitaire"],
                                        "Prix total": pre_data_2["Prix total"],
                                        "Nom du fournisseur": pre_data_2["Nom du fournisseur"],
                                    }
                                ]
                            )
                            updated_df = pd.concat(
                                    [updated_df, new_pre_2_data], ignore_index=True
                                )
                            conn.update(worksheet="Stock", data=updated_df)    

                    if(mat_pre_3!=""):
                        try:
                    
                            mat_3_to_update_id=float(mat_pre_3.split(" - ")[0].strip())
                        except:
                            mat_3_to_update_id=""
                            pass
                        # print("--------updated_df[ID]---------- :  ",updated_df["ID"],"\n-----------------mat_3_to_update_id------------------ : ",mat_3_to_update_id)
                        pre_data_3 = updated_df[updated_df["ID"] == mat_3_to_update_id].iloc[
                        0
                        ]
                        # print("--------------pre_data_3[Quantité]------------\n",type(pre_data_3["Quantité"]),"\n--------quantite_3------------\n",type(quantite_3),"\n-----------")
                        
                        if(mat_3_to_update_id!=""):
                            updated_df.drop(
                                updated_df[
                                    updated_df["ID"] == mat_3_to_update_id
                                ].index,
                                inplace=True,
                            )
                            # Creating updated data entry
                            new_pre_3_data = pd.DataFrame(
                                [
                                    {
                                        "ID":mat_3_to_update_id,
                                        "Nom du produit": pre_data_3["Nom du produit"],
                                        "Couleur": pre_data_3["Couleur"],
                                        "Date": pre_data_3["Date"],
                                        "Quantité": float(pre_data_3["Quantité"])-float(quantite_3),
                                        "Prix unitaire": pre_data_3["Prix unitaire"],
                                        "Prix total": pre_data_3["Prix total"],
                                        "Nom du fournisseur": pre_data_3["Nom du fournisseur"],
                                    }
                                ]
                            )
                            updated_df = pd.concat(
                                    [updated_df, new_pre_3_data], ignore_index=True
                                )
                            conn.update(worksheet="Stock", data=updated_df)    
                    if(mat_pre_4!=""):
                        try:
                    
                            mat_4_to_update_id=float(mat_pre_4.split(" - ")[0].strip())
                        except:
                            mat_4_to_update_id=""
                            pass
                        # print("--------updated_df[ID]---------- :  ",updated_df["ID"],"\n-----------------mat_4_to_update_id------------------ : ",mat_4_to_update_id)
                        pre_data_4 = updated_df[updated_df["ID"] == mat_4_to_update_id].iloc[
                        0
                        ]
                        # print("--------------pre_data_4[Quantité]------------\n",type(pre_data_4["Quantité"]),"\n--------quantite_4------------\n",type(quantite_4),"\n-----------")
                        
                        if(mat_4_to_update_id!=""):
                            updated_df.drop(
                                updated_df[
                                    updated_df["ID"] == mat_4_to_update_id
                                ].index,
                                inplace=True,
                            )
                            # Creating updated data entry
                            new_pre_4_data = pd.DataFrame(
                                [
                                    {
                                        "ID":mat_4_to_update_id,
                                        "Nom du produit": pre_data_4["Nom du produit"],
                                        "Couleur": pre_data_4["Couleur"],
                                        "Date": pre_data_4["Date"],
                                        "Quantité": float(pre_data_4["Quantité"])-float(quantite_4),
                                        "Prix unitaire": pre_data_4["Prix unitaire"],
                                        "Prix total": pre_data_4["Prix total"],
                                        "Nom du fournisseur": pre_data_4["Nom du fournisseur"],
                                    }
                                ]
                            )
                            updated_df = pd.concat(
                                    [updated_df, new_pre_4_data], ignore_index=True
                                )
                            conn.update(worksheet="Stock", data=updated_df)    
                    if(mat_pre_5!=""):
                        try:
                    
                            mat_5_to_update_id=float(mat_pre_5.split(" - ")[0].strip())
                        except:
                            mat_5_to_update_id=""
                            pass
                        # print("--------updated_df[ID]---------- :  ",updated_df["ID"],"\n-----------------mat_5_to_update_id------------------ : ",mat_5_to_update_id)
                        pre_data_5 = updated_df[updated_df["ID"] == mat_5_to_update_id].iloc[
                        0
                        ]
                        # print("--------------pre_data_5[Quantité]------------\n",type(pre_data_5["Quantité"]),"\n--------quantite_5------------\n",type(quantite_5),"\n-----------")
                        
                        if(mat_5_to_update_id!=""):
                            updated_df.drop(
                                updated_df[
                                    updated_df["ID"] == mat_5_to_update_id
                                ].index,
                                inplace=True,
                            )
                            # Creating updated data entry
                            new_pre_5_data = pd.DataFrame(
                                [
                                    {
                                        "ID":mat_5_to_update_id,
                                        "Nom du produit": pre_data_5["Nom du produit"],
                                        "Couleur": pre_data_5["Couleur"],
                                        "Date": pre_data_5["Date"],
                                        "Quantité": float(pre_data_5["Quantité"])-float(quantite_5),
                                        "Prix unitaire": pre_data_5["Prix unitaire"],
                                        "Prix total": pre_data_5["Prix total"],
                                        "Nom du fournisseur": pre_data_5["Nom du fournisseur"],
                                    }
                                ]
                            )
                            updated_df = pd.concat(
                                    [updated_df, new_pre_5_data], ignore_index=True
                                )
                            conn.update(worksheet="Stock", data=updated_df)
                    if(mat_pre_6!=""):
                        try:
                    
                            mat_6_to_update_id=float(mat_pre_6.split(" - ")[0].strip())
                        except:
                            mat_6_to_update_id=""
                            pass
                        # print("--------updated_df[ID]---------- :  ",updated_df["ID"],"\n-----------------mat_6_to_update_id------------------ : ",mat_6_to_update_id)
                        pre_data_6 = updated_df[updated_df["ID"] == mat_6_to_update_id].iloc[
                        0
                        ]
                        # print("--------------pre_data_6[Quantité]------------\n",type(pre_data_6["Quantité"]),"\n--------quantite_6------------\n",type(quantite_6),"\n-----------")
                        
                        if(mat_6_to_update_id!=""):
                            updated_df.drop(
                                updated_df[
                                    updated_df["ID"] == mat_6_to_update_id
                                ].index,
                                inplace=True,
                            )
                            # Creating updated data entry
                            new_pre_6_data = pd.DataFrame(
                                [
                                    {
                                        "ID":mat_6_to_update_id,
                                        "Nom du produit": pre_data_6["Nom du produit"],
                                        "Couleur": pre_data_6["Couleur"],
                                        "Date": pre_data_6["Date"],
                                        "Quantité": float(pre_data_6["Quantité"])-float(quantite_6),
                                        "Prix unitaire": pre_data_6["Prix unitaire"],
                                        "Prix total": pre_data_6["Prix total"],
                                        "Nom du fournisseur": pre_data_6["Nom du fournisseur"],
                                    }
                                ]
                            )
                            updated_df = pd.concat(
                                    [updated_df, new_pre_6_data], ignore_index=True
                                )
                            conn.update(worksheet="Stock", data=updated_df)
                st.success("Mise à jour avec succès !")
                         

    st.dataframe(existing_data)
if action == "Fournisseurs":
    with st.form(key="AYD_form"):
        # Fetch existing data
        existing_data = conn.read(worksheet="Fournisseurs", usecols=list(range(6)), ttl=5)
        existing_data = existing_data.dropna(how="all")
        st.markdown("Fournisseurs")
        # if(len(existing_data)>0):
        #     st.dataframe(existing_data.sort_values(by='ID Fournisseur', ascending=False))
        # else :
        #     st.dataframe(existing_data)
        
        
        if(len(existing_data)>0):
            existing_data=existing_data.sort_values(by='ID Fournisseur', ascending=False)
            
            id=existing_data["ID Fournisseur"].iloc[0]+1
            # # print("new id : ",id)
        else :
            
            id=1
            # # print("new id : ",id)
        st.markdown("Ajouter un fournisseur")
        
        fournisseur_name = st.text_input(label="Nom du fournisseur*")
        
        adresse = st.text_input(label="Adresse*")
        numero_de_telephone_1 = st.text_input(label="Numéro de téléphone 1*")
        numero_de_telephone_2 = st.text_input(label="Numéro de téléphone 2")
        description=st.text_area(label="Description")
        
        # Mark mandatory fields
        st.markdown("**Obligatoire*")
        
        submit_button = st.form_submit_button(label="Confirmer")
    
        
        # If the submit button is pressed
        if submit_button:
            # Check if all mandatory fields are filled
            if not fournisseur_name or not adresse or not numero_de_telephone_1     :
                st.warning("Assurez-vous que tous les champs obligatoires sont remplis.")
                st.stop()
            
            else:
                # Create a new row of vendor data
                matPre_data = pd.DataFrame(
                    [
                        {
                            "ID Fournisseur":id,
                            "Nom du fournisseur": fournisseur_name,
                            "Adresse": adresse,
                            "Numéro de téléphone 1": numero_de_telephone_1,
                            "Numéro de téléphone 2": numero_de_telephone_2,
                            "Description": description,
                            
                        }
                    ]
                )

                # Add the new vendor data to the existing data
                updated_df = pd.concat([existing_data, matPre_data], ignore_index=True)

                # Update Google Sheets with the new vendor data
                conn.update(worksheet="Fournisseurs", data=updated_df)

                st.success("Ajoutée avec succès.")
    
    if(len(existing_data)>0):
        st.markdown("Sélectionnez et mettez à jour.")

        four_to_update = st.selectbox(
                "Sélectionnez un fournisseur", options=(existing_data['ID Fournisseur'].astype(str) + ' - ' +existing_data["Nom du fournisseur"]).tolist()
            )
        try:
                
                four_to_update_id=float(four_to_update.split(" - ")[0].strip())
        except:
                pass
            
        four_data = existing_data[existing_data["ID Fournisseur"] == four_to_update_id].iloc[
                0
            ]
        with st.form(key="update_form"):
            
            fournisseur_name = st.text_input(label="Nom du fournisseur*",value=four_data["Nom du fournisseur"])
        
            adresse = st.text_input(label="Adresse*",value=four_data["Adresse"])
            numero_de_telephone_1 = st.text_input(label="Numéro de téléphone 1*",value=four_data["Numéro de téléphone 1"])
            numero_de_telephone_2 = st.text_input(label="Numéro de téléphone 2",value=four_data["Numéro de téléphone 2"])
            description=st.text_area(label="Description",value=four_data["Description"])
            # prix_total= st.text_input(label="Prix total*",value=four_data["Prix total"])
            # fournisseur = st.selectbox("Fournisseur*", options=FOURNISSEURS, index=FOURNISSEURS.index(four_data["Nom du fournisseur"]))
            

            st.markdown("**required*")
            update_button = st.form_submit_button(label="Mettre à jour les détails sur le fournisseur")

            if update_button:
                if not fournisseur_name or not adresse or not numero_de_telephone_1     :
                    st.warning("Assurez-vous que tous les champs obligatoires sont remplis.")
                else:
                    # Removing old entry
                    existing_data.drop(
                        existing_data[
                            existing_data["ID Fournisseur"] == four_to_update_id
                        ].index,
                        inplace=True,
                    )
                    # Creating updated data entry
                    updated_four_data = pd.DataFrame(
                        [
                            {
                            
                            "ID Fournisseur":four_to_update_id,
                            "Nom du fournisseur": fournisseur_name,
                            "Adresse": adresse,
                            "Numéro de téléphone 1": str(numero_de_telephone_1).replace("."," "),
                            "Numéro de téléphone 2": str(numero_de_telephone_2).replace("."," "),
                            "Description": description,
                            }
                        ]
                    )
                    # print(numero_de_telephone_2)
                    # Adding updated data to the dataframe
                    updated_df = pd.concat(
                        [existing_data, updated_four_data], ignore_index=True
                    )
                    conn.update(worksheet="Fournisseurs", data=updated_df)
                    st.success("Mise à jour avec succès !")
        st.dataframe(existing_data)




if action=="Ajouter Client":
    with st.form(key="AYD_form"):
        # Fetch existing data
        existing_data_clients = conn.read(worksheet="Clients", usecols=list(range(22)), ttl=5)
        existing_data_clients = existing_data_clients.dropna(how="all")
        st.markdown("Clients")
        if(len(existing_data_clients)>0):
            existing_data_clients=existing_data_clients.sort_values(by='ID Client', ascending=False)
            
            id=existing_data_clients["ID Client"].iloc[0]+1
            # print("new id : ",id)
        else :
            
            id=1
            # print("new id : ",id)
        
        GOUVERNORATS=[
            "",
            "Zaghouan",
            "Tunis",
            "Tozeur",
            "Tataouine",
            "Sousse",
            "Siliana",
            "Sidi Bouzid",
            "Sfax",
            "Nabeul",
            "Monastir",
            "Médenine",
            "Manouba",
            "Mahdia",
            "Kef",
            "Kébili",
            "Kasserine",
            "Kairouan",
            "Jendouba",
            "Gafsa",
            "Gabès",
            "Bizerte",
            "Ben Arous",
            "Béja",
            "Ariana",
        ]
        STATUS = [
            "En attente",
            "En cours",
            "Terminé",
            "Annulé",
            "Retour",
           
        ]
        Nom_client=st.text_input(label="Nom du client*")
        gouvernorat = st.selectbox("Gouvernorat*", options=GOUVERNORATS)
        adresse=st.text_input(label="Adresse*")
        phone_1=st.text_input(label="Numéro de téléphone 1*")
        phone_2=st.text_input(label="Numéro de téléphone 2")
        prix=st.text_input(label="Prix (avec livraison)*")
        
        status= st.selectbox("Status*", options=STATUS, index=None)
        commentaire=st.text_area(label="Commentaire")
        date = st.date_input(label="Date*")

        produit_1=st.text_input(label="Produit 1*")
        taille_1=st.text_input(label="Taille 1*")
        quantite_1=st.text_input(label="Quantité 1*")

        produit_2=st.text_input(label="Produit 2")
        taille_2=st.text_input(label="Taille 2")
        quantite_2=st.text_input(label="Quantité 2")

        produit_3=st.text_input(label="Produit 3")
        taille_3=st.text_input(label="Taille 3")
        quantite_3=st.text_input(label="Quantité 3")

        produit_4=st.text_input(label="Produit 4")
        taille_4=st.text_input(label="Taille 4")
        quantite_4=st.text_input(label="Quantité 4")

       
        
            
        submit_button_client = st.form_submit_button(label="Confirmer")

        if submit_button_client:
            # Check if all mandatory fields are filled
            if not Nom_client or not gouvernorat or not adresse  or not phone_1 or not prix or not taille_1 or not produit_1  or not quantite_1 :
                st.warning("Assurez-vous que tous les champs obligatoires sont remplis.")
                st.stop()
            
            else:
                # Create a new row of vendor data
                if status=="Terminé":
                    # revenu
                    existing_data_rev = conn.read(worksheet="Revenu", usecols=list(range(6)), ttl=5)
                    existing_data_rev= existing_data_rev.dropna(how="all")
                                     
                    if(len(existing_data_rev)>0):
                        existing_data_rev=existing_data_rev.sort_values(by='ID', ascending=False)                      
                        id_rev=existing_data_rev["ID"].iloc[0]+1                       
                    else :
                        id_rev=1

                    # --------------------------------
                    prix_livraison=8
                    ven_data_new = pd.DataFrame(
                    [
                        {
                            "ID Vente":id_rev,
                            "Montant": float(prix)-prix_livraison,    
                            "Source":Nom_client,                        
                            "Date": date.strftime("%Y-%m-%d")                           
                        }
                    ]
                    )
                    updated_df_new_rev = pd.concat([existing_data_rev, ven_data_new], ignore_index=True)
                    conn.update(worksheet="Revenu", data=updated_df_new_rev)  
                    # --------------------------------------------------------------


                    existing_data_ven = conn.read(worksheet="Ventes", usecols=list(range(15)), ttl=5)
                    existing_data_ven= existing_data_ven.dropna(how="all")
                    
                    
                    if(len(existing_data_ven)>0):
                        existing_data_ven=existing_data_ven.sort_values(by='ID Vente', ascending=False)                        
                        id_ven=existing_data_ven["ID Vente"].iloc[0]+1                        
                    else :                        
                        id_ven=1
                        
                    ven_data_new = pd.DataFrame(
                    [
                        {
                            "ID Vente":id_ven,
                            "Nom du produit fini": produit_1,                            
                            "Date": date.strftime("%Y-%m-%d")                           
                        }
                    ]
                    )
                    updated_df_new_ven = pd.concat([existing_data_ven, ven_data_new], ignore_index=True)
                    
                    if(produit_2!=""):
                        ven_data_new = pd.DataFrame(
                        [
                            {
                                "ID Vente":id_ven,
                                "Nom du produit fini": produit_2,                               
                                "Date": date.strftime("%Y-%m-%d")              
                            }
                        ])
                        updated_df_new_ven = pd.concat([existing_data_ven, ven_data_new], ignore_index=True)
                    if(produit_3!=""):
                        ven_data_new = pd.DataFrame(
                        [
                            {
                                "ID Vente":id_ven,
                                "Nom du produit fini": produit_3,                               
                                "Date": date.strftime("%Y-%m-%d")                         
                            }
                        ])
                        updated_df_new_ven = pd.concat([existing_data_ven, ven_data_new], ignore_index=True)
                    if(produit_4!=""):
                        ven_data_new = pd.DataFrame(
                        [
                            {
                                "ID Vente":id_ven,
                                "Nom du produit fini": produit_4,
                                
                                "Date": date.strftime("%Y-%m-%d")
    
                            }
                        ])
                        updated_df_new_ven = pd.concat([existing_data_ven, ven_data_new], ignore_index=True)
                    
                    
                    conn.update(worksheet="Ventes", data=updated_df_new_ven)    
                  




                client_data = pd.DataFrame(
                    [
                        {
                            "ID Client":id,
                            "Nom du client":Nom_client,
                            "Gouvernorat": gouvernorat,
                            "Adresse": adresse,
                            "Téléphone 1": str(phone_1).replace("."," "),
                            "Téléphone 2": str(phone_2).replace("."," "),
                            
                            "Montant total":prix,
                            "Status":status,
                            "Commentaire": commentaire,
                            "Date":date.strftime("%Y-%m-%d"),
                            "Produit 1":produit_1,
                            "Taille 1":taille_1,
                            "Quantité 1":quantite_1,
                            "Produit 2":produit_2,
                            "Taille 2":taille_2,
                            "Quantité 2":quantite_2,
                            "Produit 3":produit_3,
                            "Taille 3":taille_3,
                            "Quantité 3":quantite_3,
                            "Produit 4":produit_4,
                            "Taille 4":taille_4,
                            "Quantité 4":quantite_4,
                        

                        }
                    ]
                )

                # Add the new vendor data to the existing data
                existing_data_clients = pd.concat([existing_data_clients, client_data], ignore_index=True)

                # Update Google Sheets with the new vendor data
                conn.update(worksheet="Clients", data=existing_data_clients)

                st.success("Ajoutée avec succès.")
        
    if(len(existing_data_clients)>0):
            st.markdown("Sélectionnez et mettez à jour.")

            client_to_update = st.selectbox(
                    "Sélectionnez un client", options=(existing_data_clients['ID Client'].astype(str) + ' - ' +existing_data_clients["Nom du client"]).tolist()
                )
            try:
                    
                    client_to_update_id=float(client_to_update.split(" - ")[0].strip())
            except:
                    pass
                
            pre_data = existing_data_clients[existing_data_clients["ID Client"] == client_to_update_id].iloc[
                    0
                ]
            with st.form(key="update_form"):
                
                Nom_client=st.text_input(label="Nom du client*", value=pre_data["Nom du client"])
                gouvernorat = st.selectbox("Gouvernorat*", options=GOUVERNORATS)
                adresse=st.text_input(label="Adresse*", value=pre_data["Adresse"])
                phone_1=st.text_input(label="Numéro de téléphone 1*", value=pre_data["Téléphone 1"])
                phone_2=st.text_input(label="Numéro de téléphone 2", value=pre_data["Téléphone 2"])
                prix=st.text_input(label="Prix (avec livraison)*", value=pre_data["Montant total"])
                
                status= st.selectbox("Status*", options=STATUS, index=None)
                commentaire=st.text_area(label="Commentaire", value=pre_data["Commentaire"])
                date = st.date_input(label="Date*",value=pd.to_datetime(pre_data["Date"]))

                produit_1=st.text_input(label="Produit 1*", value=pre_data["Produit 1"])
                taille_1=st.text_input(label="Taille 1*", value=pre_data["Taille 1"])
                quantite_1=st.text_input(label="Quantité 1*", value=pre_data["Quantité 1"])

                produit_2=st.text_input(label="Produit 2", value=pre_data["Produit 2"])
                taille_2=st.text_input(label="Taille 2", value=pre_data["Taille 2"])
                quantite_2=st.text_input(label="Quantité 2", value=pre_data["Quantité 2"])

                produit_3=st.text_input(label="Produit 3", value=pre_data["Produit 3"])
                taille_3=st.text_input(label="Taille 3", value=pre_data["Taille 3"])
                quantite_3=st.text_input(label="Quantité 3", value=pre_data["Quantité 3"])

                produit_4=st.text_input(label="Produit 4", value=pre_data["Produit 4"])
                taille_4=st.text_input(label="Taille 4", value=pre_data["Taille 4"])
                quantite_4=st.text_input(label="Quantité 4", value=pre_data["Quantité 4"])

                st.markdown("**required*")
                update_button = st.form_submit_button(label="Mettre à jour les détails sur le fournisseur")

                if update_button:
                    if not Nom_client or not gouvernorat or not adresse  or not phone_1 or not prix or not taille_1 or not produit_1  or not quantite_1 :
                        st.warning("Assurez-vous que tous les champs obligatoires sont remplis.")
                    else:
                        # Removing old entry
                        existing_data_clients.drop(
                            existing_data_clients[
                                existing_data_clients["ID Client"] == client_to_update_id
                            ].index,
                            inplace=True,
                        )
                        # Creating updated data entry
                        updated_pre_data = pd.DataFrame(
                            [
                                {
                                     
                                    "ID Client":client_to_update_id,
                                    "Nom du client":Nom_client,
                                    "Gouvernorat": gouvernorat,
                                    "Adresse": adresse,
                                    "Téléphone 1": str(phone_1).replace("."," "),
                                    "Téléphone 2": str(phone_2).replace("."," "),
                                    
                                    "Montant total":prix,
                                    "Status":status,
                                    "Commentaire": commentaire,
                                    "Date":date.strftime("%Y-%m-%d"),
                                    "Produit 1":produit_1,
                                    "Taille 1":taille_1,
                                    "Quantité 1":quantite_1,
                                    "Produit 2":produit_2,
                                    "Taille 2":taille_2,
                                    "Quantité 2":quantite_2,
                                    "Produit 3":produit_3,
                                    "Taille 3":taille_3,
                                    "Quantité 3":quantite_3,
                                    "Produit 4":produit_4,
                                    "Taille 4":taille_4,
                                    "Quantité 4":quantite_4,
                                }
                            ]
                        )
                        # Adding updated data to the dataframe
                        updated_df = pd.concat(
                            [existing_data_clients, updated_pre_data], ignore_index=True
                        )
                        conn.update(worksheet="Clients", data=updated_df)
                        st.success("Mise à jour avec succès !")
                        if(status=="Retour"):
                            existing_data_stock = conn.read(worksheet="Stock", usecols=list(range(8)), ttl=5)
                            existing_data_stock = existing_data_stock.dropna(how="all")
                            
                            if(len(existing_data_stock)>0):
                                existing_data_stock=existing_data_stock.sort_values(by='ID', ascending=False)
                                
                                id_stock=existing_data_stock["ID"].iloc[0]+1
                               
                            else :
                                
                                id_stock=1
                            matPre_data = pd.DataFrame(
                                [
                                    {
                                        "ID":id,
                                        "Nom du produit": produit_1,
                                        
                                        "Date": date.strftime("%Y-%m-%d"),
                                        "Quantité":quantite_1,
                                        "Taille":taille_1,
                                        
                                        "Nom du fournisseur": "Retour "+str(Nom_client),
                                    }
                                ]
                            )
                            
                            # Add the new vendor data to the existing data
                            updated_df = pd.concat([existing_data_stock, matPre_data], ignore_index=True)
                            if produit_2!="":
                                id=id+1
                                matPre_data = pd.DataFrame(
                                [
                                    {
                                        "ID":id,
                                        "Nom du produit": produit_2,
                                        
                                        "Date": date.strftime("%Y-%m-%d"),
                                        "Quantité":quantite_2,
                                        "Taille":taille_2,
                                        
                                        "Nom du fournisseur": "Retour "+str(Nom_client),
                                    }
                                ]
                                 )
                            
                                # Add the new vendor data to the existing data
                                updated_df = pd.concat([existing_data_stock, matPre_data], ignore_index=True)
                            if produit_3!="":
                                id=id+1
                                matPre_data = pd.DataFrame(
                                [
                                    {
                                        "ID":id,
                                        "Nom du produit": produit_3,
                                        
                                        "Date": date.strftime("%Y-%m-%d"),
                                        "Quantité":quantite_3,
                                        "Taille":taille_3,
                                        
                                        "Nom du fournisseur": "Retour "+str(Nom_client),
                                    }
                                ]
                                 )
                            
                                # Add the new vendor data to the existing data
                                updated_df = pd.concat([existing_data_stock, matPre_data], ignore_index=True)
                            if produit_4!="":
                                id=id+1
                                matPre_data = pd.DataFrame(
                                [
                                    {
                                        "ID":id,
                                        "Nom du produit": produit_4,
                                        
                                        "Date": date.strftime("%Y-%m-%d"),
                                        "Quantité":quantite_4,
                                        "Taille":taille_4,
                                        
                                        "Nom du fournisseur": "Retour "+str(Nom_client),
                                    }
                                ]
                                 )
                            
                                # Add the new vendor data to the existing data
                                updated_df = pd.concat([existing_data_stock, matPre_data], ignore_index=True)
                            # Update Google Sheets with the new vendor data
                            conn.update(worksheet="Stock", data=updated_df)

                            # st.success("Matière première en stock ajoutée avec succès.")

    st.dataframe(existing_data_clients)
if action=="Revenu":
    with st.form(key="AYD_form"):
        # Fetch existing data
        existing_data_revu = conn.read(worksheet="Revenu", usecols=list(range(6)), ttl=5)
        existing_data_revu = existing_data_revu.dropna(how="all")
        st.markdown("Revenu")
        if(len(existing_data_revu)>0):
            existing_data_revu=existing_data_revu.sort_values(by='ID', ascending=False)
            
            id=existing_data_revu["ID"].iloc[0]+1
            # print("new id : ",id)
        else :
            
            id=1
            # print("new id : ",id)
       
        st.markdown("Ajouter une revenu")
        
        montant = st.text_input(label="Montant*")
        
        source = st.text_input(label="Source*")
        date = st.date_input(label="Date*")

        num_fact = st.text_input(label="Numéro de facture")
        commentaire=st.text_area(label="Commentaire")    
        # Mark mandatory fields

        st.markdown("**Obligatoire*")
        
        submit_button = st.form_submit_button(label="Confirmer")
    
        
        # If the submit button is pressed
        if submit_button:
            # Check if all mandatory fields are filled
            if not montant or not source or not date :
                st.warning("Assurez-vous que tous les champs obligatoires sont remplis.")
                st.stop()
            # elif existing_data_revu["CompanyName"].str.contains(company_name).any():
            #     st.warning("A vendor with this company name already exists.")
            #     st.stop()
            else:
                
                # Create a new row of vendor data
                revu_data = pd.DataFrame(
                    [
                        {
                            "ID":id,
                            "Montant": str(montant).replace("."," "),
                            "Source": source,
                            "Date": date.strftime("%Y-%m-%d"),
                            "Numéro de facture": str(num_fact).replace("."," "),
                            "Commentaire":commentaire,
                            
                        }
                    ]
                )

                # Add the new vendor data to the existing data
                updated_df = pd.concat([existing_data_revu, revu_data], ignore_index=True)

                # Update Google Sheets with the new vendor data
                conn.update(worksheet="Revenu", data=updated_df)

                st.success("Ajoutée avec succès.")
    # if(len(existing_data_revu)>0):
    #     mat_to_delete = st.selectbox(
    #             "Sélectionnez une matière première à supprimer", options=(existing_data_revu['ID'].astype(str) + ' - ' +existing_data_revu["Nom du produit"]+ ' - ' +existing_data_revu["Couleur"]+ ' - ' +existing_data_revu["Date"]).tolist()
    #             # existing_data_revu["ID"].tolist()+existing_data_revu["Nom du produit"].tolist()
    #         )
    #     try:
            
    #         mat_to_delete_id=float(mat_to_delete.split(" - ")[0].strip())
    #     except:
    #         pass
    #     if st.button("Supprimer"):
                
    #             existing_data_revu.drop(
    #                 existing_data_revu[existing_data_revu["ID"] == mat_to_delete_id].index,
    #                 inplace=True,
    #             )
            
    #             conn.update(worksheet="Stock", data=existing_data_revu)
    #             st.success("Matière première supprimée avec succès !")
    
    

    if(len(existing_data_revu)>0):
        st.markdown("Sélectionnez et mettez à jour.")

        rev_to_update = st.selectbox(
                "Sélectionnez", options=(existing_data_revu['ID'].astype(str) + ' - ' +existing_data_revu["Montant"].astype(str)+ ' - ' +existing_data_revu["Source"]+ ' - ' +existing_data_revu["Date"]).tolist()
            )
        try:
                
                rev_to_update_id=float(rev_to_update.split(" - ")[0].strip())
        except:
                pass
            
        pre_data = existing_data_revu[existing_data_revu["ID"] == rev_to_update_id].iloc[
                0
            ]
        with st.form(key="update_form"):
            
            
            montant = st.text_input(label="Montant*", value=pre_data["Montant"])
        
            source = st.text_input(label="Source*", value=pre_data["Source"])
            date = st.date_input(label="Date*", value=pd.to_datetime(pre_data["Date"]))

            num_fact = st.text_input(label="Numéro de facture", value=pre_data["Numéro de facture"])
            commentaire=st.text_area(label="Commentaire", value=pre_data["Commentaire"])

            st.markdown("**required*")
            update_button = st.form_submit_button(label="Mettre à jour")

            if update_button:
                if not montant or not source or not date :
                    st.warning("Assurez-vous que tous les champs obligatoires sont remplis.")
                    st.stop()
                else:
                    # Removing old entry
                    existing_data_revu.drop(
                        existing_data_revu[
                            existing_data_revu["ID"] == rev_to_update_id
                        ].index,
                        inplace=True,
                    )
                    # Creating updated data entry
                    updated_pre_data = pd.DataFrame(
                        [
                            {
                            "ID":rev_to_update_id,
                            "Montant": str(montant).replace("."," "),
                            "Source": source,
                            "Date": date.strftime("%Y-%m-%d"),
                            "Numéro de facture": str(num_fact).replace("."," "),
                            "Commentaire":commentaire,
                            }
                        ]
                    )
                    # Adding updated data to the dataframe
                    updated_df = pd.concat(
                        [existing_data_revu, updated_pre_data], ignore_index=True
                    )
                    conn.update(worksheet="Revenu", data=updated_df)
                    st.success("Mise à jour avec succès !")
    st.dataframe(existing_data_revu)
if action=="Dépenses":
    with st.form(key="AYD_form"):
        # Fetch existing data
        existing_data_dep = conn.read(worksheet="Dépenses", usecols=list(range(6)), ttl=5)
        existing_data_dep = existing_data_dep.dropna(how="all")
        st.markdown("Dépenses")
        if(len(existing_data_dep)>0):
            existing_data_dep=existing_data_dep.sort_values(by='ID', ascending=False)
            
            id=existing_data_dep["ID"].iloc[0]+1
            
        else :
            
            id=1
            
       
        st.markdown("Ajouter une dépense")
        
        montant = st.text_input(label="Montant*")
        
        source = st.text_input(label="Source*")
        date = st.date_input(label="Date*")

        num_fact = st.text_input(label="Numéro de facture")
        commentaire=st.text_area(label="Commentaire")    
        # Mark mandatory fields

        st.markdown("**Obligatoire*")
        
        submit_button = st.form_submit_button(label="Confirmer")
    
        
        # If the submit button is pressed
        if submit_button:
            # Check if all mandatory fields are filled
            if not montant or not source or not date :
                st.warning("Assurez-vous que tous les champs obligatoires sont remplis.")
                st.stop()
            # elif existing_data_dep["CompanyName"].str.contains(company_name).any():
            #     st.warning("A vendor with this company name already exists.")
            #     st.stop()
            else:
                
                # Create a new row of vendor data
                revu_data = pd.DataFrame(
                    [
                        {
                            "ID":id,
                            "Montant": str(montant).replace("."," "),
                            "Source": source,
                            "Date": date.strftime("%Y-%m-%d"),
                            "Numéro de facture": str(num_fact).replace("."," "),
                            "Commentaire":commentaire,
                            
                        }
                    ]
                )

                # Add the new vendor data to the existing data
                updated_df = pd.concat([existing_data_dep, revu_data], ignore_index=True)

                # Update Google Sheets with the new vendor data
                conn.update(worksheet="Revenu", data=updated_df)

                st.success("Ajoutée avec succès.")
    # if(len(existing_data_dep)>0):
    #     mat_to_delete = st.selectbox(
    #             "Sélectionnez une matière première à supprimer", options=(existing_data_dep['ID'].astype(str) + ' - ' +existing_data_dep["Nom du produit"]+ ' - ' +existing_data_dep["Couleur"]+ ' - ' +existing_data_dep["Date"]).tolist()
    #             # existing_data_dep["ID"].tolist()+existing_data_dep["Nom du produit"].tolist()
    #         )
    #     try:
            
    #         mat_to_delete_id=float(mat_to_delete.split(" - ")[0].strip())
    #     except:
    #         pass
    #     if st.button("Supprimer"):
                
    #             existing_data_dep.drop(
    #                 existing_data_dep[existing_data_dep["ID"] == mat_to_delete_id].index,
    #                 inplace=True,
    #             )
            
    #             conn.update(worksheet="Stock", data=existing_data_dep)
    #             st.success("Matière première supprimée avec succès !")
    
    

    if(len(existing_data_dep)>0):
        st.markdown("Sélectionnez et mettez à jour.")

        rev_to_update = st.selectbox(
                "Sélectionnez", options=(existing_data_dep['ID'].astype(str) + ' - ' +existing_data_dep["Montant"].astype(str)+ ' - ' +existing_data_dep["Source"]+ ' - ' +existing_data_dep["Date"]).tolist()
            )
        try:
                
                rev_to_update_id=float(rev_to_update.split(" - ")[0].strip())
        except:
                pass
            
        pre_data = existing_data_dep[existing_data_dep["ID"] == rev_to_update_id].iloc[
                0
            ]
        with st.form(key="update_form"):
            
            
            montant = st.text_input(label="Montant*", value=pre_data["Montant"])
        
            source = st.text_input(label="Source*", value=pre_data["Source"])
            date = st.date_input(label="Date*", value=pd.to_datetime(pre_data["Date"]))

            num_fact = st.text_input(label="Numéro de facture", value=pre_data["Numéro de facture"])
            commentaire=st.text_area(label="Commentaire", value=pre_data["Commentaire"])

            st.markdown("**required*")
            update_button = st.form_submit_button(label="Mettre à jour")

            if update_button:
                if not montant or not source or not date :
                    st.warning("Assurez-vous que tous les champs obligatoires sont remplis.")
                    st.stop()
                else:
                    # Removing old entry
                    existing_data_dep.drop(
                        existing_data_dep[
                            existing_data_dep["ID"] == rev_to_update_id
                        ].index,
                        inplace=True,
                    )
                    # Creating updated data entry
                    updated_pre_data = pd.DataFrame(
                        [
                            {
                            "ID":rev_to_update_id,
                            "Montant": str(montant).replace("."," "),
                            "Source": source,
                            "Date": date.strftime("%Y-%m-%d"),
                            "Numéro de facture": str(num_fact).replace("."," "),
                            "Commentaire":commentaire,
                            }
                        ]
                    )
                    # Adding updated data to the dataframe
                    updated_df = pd.concat(
                        [existing_data_dep, updated_pre_data], ignore_index=True
                    )
                    conn.update(worksheet="Revenu", data=updated_df)
                    st.success("Mise à jour avec succès !")
    st.dataframe(existing_data_dep)
if action == "Fiche d'argent":
        existing_data_res = conn.read(worksheet="Fiche d'argent", usecols=list(range(3)), ttl=5)
        existing_data_res = existing_data_res.dropna(how="all")
        st.markdown("Fiche d'argent")       
        st.dataframe(existing_data_res)
    
        
            