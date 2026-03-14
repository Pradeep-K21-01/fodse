import os
from pathlib import Path
import pdfplumber

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR.parent / "datasets"
OUTPUT_PATH = BASE_DIR.parent / "processed_text"

OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

def extract_text(file_path: Path) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"                import os
                from pathlib import Path
                import pdfplumber
                
                BASE_DIR = Path(__file__).resolve().parent
                DATASET_PATH = BASE_DIR.parent / "datasets"
                OUTPUT_PATH = BASE_DIR.parent / "processed_text"
                
                OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
                
                def extract_text(file_path: Path) -> str:
                    text = ""
                    with pdfplumber.open(file_path) as pdf:
                        for page in pdf.pages:
                            content = page.extract_text()
                            if content:
                                text += content + "\n"
                    return text
                
                for file in os.listdir(DATASET_PATH):
                    if file.lower().endswith(".pdf"):
                        src = DATASET_PATH / file
                        text = extract_text(src)
                        (OUTPUT_PATH / f"{file}.txt").write_text(text, encoding="utf-8")
                
                print("PDF conversion complete.")                import os
                from pathlib import Path
                import pdfplumber
                
                BASE_DIR = Path(__file__).resolve().parent
                DATASET_PATH = BASE_DIR.parent / "datasets"
                OUTPUT_PATH = BASE_DIR.parent / "processed_text"
                
                OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
                
                def extract_text(file_path: Path) -> str:
                    text = ""
                    with pdfplumber.open(file_path) as pdf:
                        for page in pdf.pages:
                            content = page.extract_text()
                            if content:
                                text += content + "\n"
                    return text
                
                for file in os.listdir(DATASET_PATH):
                    if file.lower().endswith(".pdf"):
                        src = DATASET_PATH / file
                        text = extract_text(src)
                        (OUTPUT_PATH / f"{file}.txt").write_text(text, encoding="utf-8")
                
                print("PDF conversion complete.")                from fastapi import APIRouter
                
                router = APIRouter()
                
                @router.get("/ask")
                def ask(question: str):
                    # TODO: hook this into your RAG engine (ai/engine.py)
                    return {"answer": f"Received question: {question}"}                    from fastapi import APIRouter
                    
                    router = APIRouter()
                    
                    @router.get("/ask")
                    def ask(question: str):
                        # TODO: hook this into your RAG engine (ai/engine.py)
                        return {"answer": f"Received question: {question}"}                        from fastapi import APIRouter
                        
                        router = APIRouter()
                        
                        @router.get("/ask")
                        def ask(question: str):
                            # TODO: hook this into your RAG engine (ai/engine.py)
                            return {"answer": f"Received question: {question}"}                            from fastapi import APIRouter
                            
                            router = APIRouter()
                            
                            @router.get("/ask")
                            def ask(question: str):
                                # TODO: hook this into your RAG engine (ai/engine.py)
                                return {"answer": f"Received question: {question}"}                                from fastapi import APIRouter
                                
                                router = APIRouter()
                                
                                @router.get("/ask")
                                def ask(question: str):
                                    # TODO: hook this into your RAG engine (ai/engine.py)
                                    return {"answer": f"Received question: {question}"}                                    from fastapi import APIRouter
                                    
                                    router = APIRouter()
                                    
                                    @router.get("/ask")
                                    def ask(question: str):
                                        # TODO: hook this into your RAG engine (ai/engine.py)
                                        return {"answer": f"Received question: {question}"}                                        from fastapi import APIRouter
                                        
                                        router = APIRouter()
                                        
                                        @router.get("/ask")
                                        def ask(question: str):
                                            # TODO: hook this into your RAG engine (ai/engine.py)
                                            return {"answer": f"Received question: {question}"}                                            from fastapi import APIRouter
                                            
                                            router = APIRouter()
                                            
                                            @router.get("/ask")
                                            def ask(question: str):
                                                # TODO: hook this into your RAG engine (ai/engine.py)
                                                return {"answer": f"Received question: {question}"}                                                from fastapi import APIRouter
                                                
                                                router = APIRouter()
                                                
                                                @router.get("/ask")
                                                def ask(question: str):
                                                    # TODO: hook this into your RAG engine (ai/engine.py)
                                                    return {"answer": f"Received question: {question}"}
    return text

for file in os.listdir(DATASET_PATH):
    if file.lower().endswith(".pdf"):
        src = DATASET_PATH / file
        text = extract_text(src)
        (OUTPUT_PATH / f"{file}.txt").write_text(text, encoding="utf-8")

print("PDF conversion complete.")import os
from pathlib import Path
import pdfplumber

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR.parent / "datasets"
OUTPUT_PATH = BASE_DIR.parent / "processed_text"

OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

def extract_text(file_path: Path) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    return text

for file in os.listdir(DATASET_PATH):
    if file.lower().endswith(".pdf"):
        src = DATASET_PATH / file
        text = extract_text(src)
        (OUTPUT_PATH / f"{file}.txt").write_text(text, encoding="utf-8")

print("PDF conversion complete.")
