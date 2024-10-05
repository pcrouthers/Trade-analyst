#!/bin/bash

# Install Ollama
curl -sSL https://ollama.com/download | sh

# Pull the Phi-3 model
ollama pull gemma:2b
