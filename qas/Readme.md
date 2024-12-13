Create Virtual Env

python -m venv venv

pip install -r requirements.txt

Change line 252 in venv > Lib > site-packages > data > processors > squad.py to

pad_token_indices = np.where(np.array(span["input_ids"]) == tokenizer.pad_token_id)[0]

Start the server with uvicorn. Make sure to use the uvicorn from venv
uvicorn main:app --reload 