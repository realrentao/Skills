#!/usr/bin/env python3
"""Copy audio files to repo and generate missing ones"""
import os, shutil, glob, asyncio, subprocess

SRC = r"D:\workbuddy工作区\2026-06-10-13-51-52\意大利语考试真题\定制考题"
DST = r"D:\workbuddy工作区\2026-06-10-13-51-52\italiano-esami"

LEVELS = {"CILS": ["A1","A2","B1","B2","C1","C2"],
          "CELI": ["A1","A2","B1","B2","C1","C2"]}

def copy_existing():
    for exam_type in LEVELS:
        for level in LEVELS[exam_type]:
            src_dir = os.path.join(SRC, exam_type, level, "audio")
            dst_dir = os.path.join(DST, exam_type, level, "audio")
            os.makedirs(dst_dir, exist_ok=True)
            
            if os.path.exists(src_dir):
                count = 0
                for f in glob.glob(os.path.join(src_dir, "*.mp3")):
                    shutil.copy2(f, dst_dir)
                    count += 1
                print("{} {}: {} files copied".format(exam_type, level, count))
            else:
                print("{} {}: no source dir".format(exam_type, level))

# Missing audio scripts for CELI
MISSING = {
    "CELI B2 ascolto2": "Per migliorare il sistema scolastico, gli esperti raccomandano di ridurre il numero di studenti per classe e di introdurre tecnologie digitali innovative nelle aule. Queste riforme potrebbero migliorare significativamente la qualità dell'apprendimento.",
    "CELI B2 ascolto4": "La casa del signor Rossi è un esempio perfetto di edilizia sostenibile. Con i suoi pannelli solari e il sistema di raccolta dell'acqua piovana, riesce a ridurre le emissioni di CO2 dell'ottanta per cento rispetto a una casa tradizionale.",
    "CELI C1 ascolto2": "Tra le misure più efficaci per migliorare la mobilità urbana, il relatore cita le zone a traffico limitato, che hanno dimostrato di ridurre significativamente l'inquinamento nelle aree urbane. Molte città italiane le stanno adottando con buoni risultati.",
    "CELI C1 ascolto3": "Secondo il relatore, ciò che manca è una visione organica a livello nazionale. Le iniziative sono troppo frammentate e manca un coordinamento efficace tra i diversi livelli istituzionali per affrontare il problema in modo sistemico.",
    "CELI C1 ascolto4": "La critica principale mossa al sistema attuale è la mancanza di coordinamento tra le varie iniziative. Ogni città procede per conto proprio, senza una strategia comune che permetta di massimizzare i risultati degli investimenti."
}

async def gen_missing():
    VOICE = "it-IT-IsabellaNeural"
    print("\nGenerating missing audio files...")
    
    for key, text in MISSING.items():
        parts = key.split()
        exam_type = parts[0]
        level = parts[1]
        item_num = parts[2].replace("ascolto", "")
        
        dst_dir = os.path.join(DST, exam_type, level, "audio")
        os.makedirs(dst_dir, exist_ok=True)
        
        # Generate with unique name
        fname = "ascolto_{}_{}.mp3".format(item_num, level.lower())
        fpath = os.path.join(dst_dir, fname)
        
        if os.path.exists(fpath) and os.path.getsize(fpath) > 1000:
            print("  SKIP {} (exists)".format(fname))
            continue
        
        print("  Generating {}...".format(fname), end=" ", flush=True)
        proc = await asyncio.create_subprocess_exec(
            "edge-tts", "--voice", VOICE, "--rate", "+5%", "--text", text,
            "--write-media", fpath,
            stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL
        )
        await proc.communicate()
        size = os.path.getsize(fpath) if os.path.exists(fpath) else 0
        print("{}KB {}".format(size//1024, "OK" if size > 1000 else "FAIL"))

def main():
    print("=" * 60)
    print("Setting up audio files")
    print("=" * 60)
    
    copy_existing()
    asyncio.run(gen_missing())
    
    # Summary
    print("\n=== Audio files in repo ===")
    for exam_type in LEVELS:
        for level in LEVELS[exam_type]:
            d = os.path.join(DST, exam_type, level, "audio")
            if os.path.exists(d):
                files = glob.glob(os.path.join(d, "*.mp3"))
                print("{} {}: {} files ({}KB total)".format(
                    exam_type, level, len(files),
                    sum(os.path.getsize(f) for f in files)//1024))

if __name__ == "__main__":
    main()
