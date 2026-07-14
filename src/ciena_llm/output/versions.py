from typing import Dict

from importlib.metadata import version

from ollama import Client
import urllib
import socket

class VersionExtractor:
    def __init__(self, extractor: "ClimateImpactExtractor"):
        self.extractor = extractor
        self.ollama_client = Client()

    def extract_libraries_versions(self) -> Dict[str, str]:
        libs=["ciena_llm",
              "ollama",
              "langchain_protocol","langchain_ollama","langchain_core",
              "pydantic_core","pydantic","pylint_pydantic","pylint_plugin_utils",
              "tokenizers","transformers",
              "langsmith", 
              ]
        versions = {}
        for lib in libs:
            lib_version = self.extract_lib_version(lib)
            versions[lib] = lib_version
        
        return versions

    def extract_lib_version(self, lib: str) -> str:
        l_version:str
        try:
            l_version = version(lib)
        except ImportError as e:
            l_version = "not installed"
        return l_version
    
    def extract_ollama_data(self) -> dict:
        model_name = self.extractor.config.get("llm", {}).get("name", None)

        o_version = self.extract_ollama_version()

        o_model_info = None
        if model_name is not None:
            o_model_info = self.extract_ollama_model_info(model_name)

        o_base_url = self.extract_ollama_host()
        return {
            "version": o_version,
            "model_info": o_model_info,
            "host": o_base_url
        }
    

    def extract_ollama_model_info(self, model_name:str) -> dict:
        models_info = self.ollama_client.list()
        #print(f"Ollama model info for {model_name}: {model_info}")
        for model in models_info.models:
            if model.model == model_name:
                quantization_level=None
                if hasattr(model, "details") and hasattr(model.details, "quantization_level"):
                    quantization_level = model.details.quantization_level
                return {"model": model.model, "digest": model.digest,"quantization_level": quantization_level}

        
        return None
    

    def extract_ollama_version(self) -> str:
        ollama_version = self.ollama_client._request(dict,"GET", "/api/version").get("version", "unknown")
        return ollama_version
    
    def extract_ollama_host(self) -> str:
        host = None
        if hasattr(self.ollama_client, '_client') and hasattr(self.ollama_client._client, '_base_url'):
            host = str(self.ollama_client._client._base_url)
        else:
            return "unknown"
        host_url =  urllib.parse.urlsplit(host)

        if "127.0.0." in host_url.hostname or "localhost" in host_url.hostname:           
            host =host_url.scheme + "://" + socket.gethostname() + ":" + str(host_url.port)
        return host