# What's MyMemoryGPT ?

(French below)

MyMemoryGPT is a tool which allows you to create a digital local memory composed of your files, and allow GPT to use this memory to answer your questions with relevant documents from your memory in the context.

MyMemoryGPT don't send all your documents to OpenAI. It only select the most relevant documents based on your request, then send your question to GPT with the documents in context. 

To sump up, it's like if GPT had all the personnal documents in his local memory and use them to provide more relevant answers.

# How to install MyMemoryGPT ?

This tutorial works for Debian based systems, but it should works on Windows/MacOS since it's only based on python. You will just have to search the equivalent for your system.

First, clone this repository, open a terminal and move to the MyMemoryGPT folder.

Now create a virtual environnement, and install the requirements (can take a few minutes depending on your internet speed)

> virtualenv venv
>
> source venv/bin/activate
>
> pip3 install -r requirements.txt

Now you can use MyMemoryGPT.

# How to use MyMemoryGPT ?

Add your OpenAI API key inside the query_gpt.py file in the appropriate spot (You won't be able to ask questions without it). You can also change the model used to answer your questions (default is gpt-4o-mini).

If you haven't already loaded documents inside your memory, or if you want to add more documents, do this.

Open a terminal, move to your MyMemoryGPT folder and activate your virtual environnement (you can use the terminal used for installation).

> source venv/bin/activate

Copy all the documents you want to load into your memory inside the "documents" folder.

⚠️ Please note that MyMemoryGPT currently only support .txt files. If you want to load other files, convert them into text files and make a small sentence at the beggining of the file to specify the type of file it was, so GPT can understand it ⚠️

Now launch the index_documents.py script to load those documents inside your memory.

> python3 index_documents.py

Once the script has finished to import your files, you should see 2 new files in your MyMemoryGPT folder: hnsw_index.bin and document_paths.txt

Note : if you want to remove documents from your memory, delete those 2 files, then delete the documents you want to remove from the "documents" folder, then run this script again to create an index without those documents.

Now to ask questions to GPT using your memory, just launch the query_gpt.py script

> python3 query_gpt.py

The script will remember your previous questions and the previous answers, but everything will be earased once you close the script, do don't do it too early.

# Qu'est-ce que MyMemoryGPT ?

MyMemoryGPT est un outil qui vous permet de créer une mémoire numérique locale composée de vos fichiers, et permet à GPT d'utiliser cette mémoire pour répondre à vos question en ayant les documents appropriés issus de votre mémoire dans son contexte.

MyMemoryGPT n'envoie pas tous vos documents à OpenAI. Il sélectionne uniquement les documents les plus appropriés en se basant sur votre question, puis transmet votre question à GPT avec ces documents en contexte. 

Pour résumer, c'est comme si GPT avait tous vos documents personnels dans sa mémoire locale, et les utilisait pour vous fournir des réponses plus précises.

# Comment installer MyMemoryGPT ?

Ce tutoriel fonctionne pour les systèmes Debian ou équivalent, mais devrait également fonctionner sur d'autres systèmes (Windows/MacOS) sachant qu'il est basé uniquement sur python. Vous aurez probablement juste à chercher l'équivalent pour votre système.

Premièrement, clonez ce dépot, ouvrez un terminal et déplacez vous vers le dossier de MyMemoryGPT.

Deuxièmement, créez un environnement virtuel et installez les prérequis (peut prendre quelques minutes en fonction de la vitesse de votre connexion)

> virtualenv venv
>
> source venv/bin/activate
>
> pip3 install -r requirements.txt

Vous pouvez désormais utiliser MyMemoryGPT.

# Comment utiliser MyMemoryGPT ?

Ajoutez votre clé API OpenAI dans le fichier query_gpt.py à l'emplacement approprié (Vous ne pourrez pas poser de questions sans cela). Vous pouvez également changer le modèle utilisé pour répondre à vos questions (le modèle utilisé par défaut est gpt-4o-mini).

Si vous n'avez pas déjà chargé des documents dans votre mémoire, ou si vous souhaitez en rajouter, faites ceci.

Ouvrez un terminal, déplacez vous vers votre dossier MyMemoryGPT et activez votre environnement virtuel (Vous pouvez utiliser le terminal utilisé précédemment pour l'installation).

> source venv/bin/activate

Copiez tous les documents que vous souhaitez charger dans votre mémoire dans le dossier "documents".

⚠️ Veuillez noter que MyMemoryGPT ne supporte actuellement que les fichiers .txt. Si vous souhaitez charger d'autres fichiers, convertissez les d'abord en fichiers texte et écrivez une petite phrase en début de fichier pour préciser à GPT de quel type de fichier il s'agit, afin qu'il puisse comprendre ⚠️

Maintenant lancez le script index_documents.py pour charger ces documents dans votre mémoire.

> python3 index_documents.py

Une fois que le script a fini de charger vos fichiers, vous devriez voir 2 nouveaux fichiers dans votre dossier MyMemoryGPT : hnsw_index.bin et document_paths.txt

Note : si vous souhaitez effacer des documents de votre mémoire, supprimez ces 2 fichiers, puis supprimez les documents souhaités du dossier "documents", puis lancez de nouveau ce script pour créer un index sans ces documents.

Maintenant, pour poser des questions à GPT en utilisant votre mémoire, lancez simplement le script query_gpt.py

> python3 query_gpt.py

Le script se souviendra de vos questions/réponses précédentes, mais tout sera effacé lorsque le script est fermé, donc ne le fermez pas trop tôt.
