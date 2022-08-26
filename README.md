# MOOD: MObility Data Privacy as Orphan Deseases

Welcome to MOOD, a centralized user-centric multi-LPPM system which protects mobility traces using 2 principles : composition of LPPMs and fine-grained protection. 

You can :
 
- Protect mobility traces with a single LPPM, namely, Geo-indistinguishability (G), Trilateration (T), and HMC (H).   .
- Protect mobility traces with multi-LPPMs, i.e., a combination of G,T, and H.
- Compute Spatio-temporal distortion metric (STD). 
- Apply fine-grained protection by splitting mobility traces with fixed time slices. 
- Run re-identification attacks (POI-Attack, PIT-Attack, and AP-Attack)

# Requirements

Install Accio
Install S2Geometry
Install java

# Format of Mobility Dataset

One mobility trace per user = CSV file named <user_id>.csv

CSV file format = Each line is a record of the mobility trace.

One record = <lattitude,longitude,timestamp>

Timestamp = Unix time POSIX

# Run main script of MOOD

bash Launcher_MooD.sh config_MooD.json <sourcefiles_path> <name_output>

In config_MooD.json, precise the path of the target mobility dataset. 

# Paper 

Khalfoun, B., Maouche, M., Ben Mokhtar, S., & Bouchenak, S. (2019, December). Mood: Mobility data privacy as orphan disease: Experimentation and deployment paper. In Proceedings of the 20th International Middleware Conference (pp. 136-148).





# Contact

besma.khalfoun@insa-lyon.fr
