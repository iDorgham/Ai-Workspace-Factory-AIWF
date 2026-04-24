import os

certs_dir = "/Users/Dorgham/Documents/Work/Devleopment/AIWF/docs/certifications"
for filename in os.listdir(certs_dir):
    if filename.endswith(".md"):
        path = os.path.join(certs_dir, filename)
        with open(path, "r") as f:
            content = f.read()
        
        content = content.replace("v13.0.0 OMEGA", "v19.0.0 OMEGA SINGULARITY")
        content = content.replace("AIWF v13.0.0 OMEGA", "AIWF v19.0.0 OMEGA SINGULARITY")
        
        with open(path, "w") as f:
            f.write(content)
