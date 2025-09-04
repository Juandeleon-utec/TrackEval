import re
import matplotlib.pyplot as plt

def parse_motchallenge_txt(filename):
    """
    Parsea el archivo txt de resultados MOTChallenge y extrae metricas en diccionarios.
    Devuelve:
    results = {
      'tracker_name': {
          'sequence': {
              'HOTA': {...},
              'CLEAR': {...},
              'Identity': {...},
              'Count': {...},
          }
      }
    }
    """
    results = {}
    current_tracker = None
    current_seq = None
    current_metric = None

    # Patrones para identificar secciones y datos
    re_eval = re.compile(r"Evaluating (.+)")
    re_hota_header = re.compile(r"HOTA: (.+)")
    re_clear_header = re.compile(r"CLEAR: (.+)")
    re_identity_header = re.compile(r"Identity: (.+)")
    re_count_header = re.compile(r"Count: (.+)")
    re_metric_line = re.compile(r"([A-Z0-9\-_]+)\s+(.+)")
    
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Detectar el nombre del tracker
        m = re_eval.match(line)
        if m:
            current_tracker = m.group(1).strip()
            if current_tracker not in results:
                results[current_tracker] = {}
            i += 1
            continue
        
        # Detectar HOTA header
        m = re_hota_header.match(line)
        if m:
            current_metric = 'HOTA'
            # La siguiente linea con valores suele ser 2 líneas despues
            # extraer keys de la línea del header (2da línea tras header)
            header_line = lines[i+1].strip().split()
            i += 2
            # Línea con datos:
            data_line = lines[i].strip()
            # extraer secuencia y valores
            parts = data_line.split()
            seq = parts[0]
            values = parts[1:]
            if seq not in results[current_tracker]:
                results[current_tracker][seq] = {}
            # Mapear clave-valor
            results[current_tracker][seq][current_metric] = {}
            for key, val in zip(header_line[1:], values):
                try:
                    results[current_tracker][seq][current_metric][key] = float(val)
                except:
                    results[current_tracker][seq][current_metric][key] = val
            i += 1
            continue

        # Detectar CLEAR header
        m = re_clear_header.match(line)
        if m:
            current_metric = 'CLEAR'
            header_line = lines[i+1].strip().split()
            i += 2
            data_line = lines[i].strip()
            parts = data_line.split()
            seq = parts[0]
            values = parts[1:]
            if seq not in results[current_tracker]:
                results[current_tracker][seq] = {}
            results[current_tracker][seq][current_metric] = {}
            for key, val in zip(header_line[1:], values):
                try:
                    results[current_tracker][seq][current_metric][key] = float(val)
                except:
                    results[current_tracker][seq][current_metric][key] = val
            i += 1
            continue

        # Detectar Identity header
        m = re_identity_header.match(line)
        if m:
            current_metric = 'Identity'
            header_line = lines[i+1].strip().split()
            i += 2
            data_line = lines[i].strip()
            parts = data_line.split()
            seq = parts[0]
            values = parts[1:]
            if seq not in results[current_tracker]:
                results[current_tracker][seq] = {}
            results[current_tracker][seq][current_metric] = {}
            for key, val in zip(header_line[1:], values):
                try:
                    results[current_tracker][seq][current_metric][key] = float(val)
                except:
                    results[current_tracker][seq][current_metric][key] = val
            i += 1
            continue

        # Detectar Count header
        m = re_count_header.match(line)
        if m:
            current_metric = 'Count'
            header_line = lines[i+1].strip().split()
            i += 2
            data_line = lines[i].strip()
            parts = data_line.split()
            seq = parts[0]
            values = parts[1:]
            if seq not in results[current_tracker]:
                results[current_tracker][seq] = {}
            results[current_tracker][seq][current_metric] = {}
            for key, val in zip(header_line[1:], values):
                try:
                    results[current_tracker][seq][current_metric][key] = float(val)
                except:
                    results[current_tracker][seq][current_metric][key] = val
            i += 1
            continue

        i += 1

    return results

def plot_metrics(results):
    """
    Genera gráficas para los trackers y secuencias contenidas en results.
    Muestra las métricas más relevantes en barras agrupadas.
    """
    for tracker, seqs in results.items():
        for seq, metrics in seqs.items():
            print(f"Tracker: {tracker} | Secuencia: {seq}")
            # HOTA
            if 'HOTA' in metrics:
                print("\nMetricas HOTA:")
                for k, v in metrics['HOTA'].items():
                    print(f"  {k}: {v:.2f}")
                keys = list(metrics['HOTA'].keys())
                values = [metrics['HOTA'][k] for k in keys]
                plt.figure(figsize=(10,5))
                plt.bar(keys, values, color='skyblue')
                plt.title(f"HOTA Metrics - {tracker} - {seq}")
                plt.xticks(rotation=45, ha='right')
                plt.ylabel('Valor (%)')
                plt.tight_layout()
                plt.show()

            # CLEAR
            if 'CLEAR' in metrics:
                print("\nMetricas CLEAR:")
                for k, v in metrics['CLEAR'].items():
                    print(f"  {k}: {v:.2f}")
                # Elegimos algunas métricas para graficar (MOTA, MOTP, IDSW, etc)
                keys_to_plot = ['MOTA', 'MOTP', 'IDSW', 'MT', 'PT', 'ML', 'Frag']
                keys = []
                values = []
                for k in keys_to_plot:
                    if k in metrics['CLEAR']:
                        keys.append(k)
                        values.append(metrics['CLEAR'][k])
                plt.figure(figsize=(10,5))
                plt.bar(keys, values, color='orange')
                plt.title(f"CLEAR MOT Metrics - {tracker} - {seq}")
                plt.xticks(rotation=45, ha='right')
                plt.ylabel('Valor / Conteo')
                plt.tight_layout()
                plt.show()

            # Identity
            if 'Identity' in metrics:
                print("\nMetricas Identity:")
                for k, v in metrics['Identity'].items():
                    print(f"  {k}: {v:.2f}")
                keys = list(metrics['Identity'].keys())
                values = [metrics['Identity'][k] for k in keys]
                plt.figure(figsize=(10,5))
                plt.bar(keys, values, color='green')
                plt.title(f"Identity Metrics - {tracker} - {seq}")
                plt.xticks(rotation=45, ha='right')
                plt.ylabel('Valor (%) o Conteo')
                plt.tight_layout()
                plt.show()

            # Count
            if 'Count' in metrics:
                print("\nConteo:")
                for k, v in metrics['Count'].items():
                    print(f"  {k}: {v:.2f}")
                keys = list(metrics['Count'].keys())
                values = [metrics['Count'][k] for k in keys]
                plt.figure(figsize=(10,5))
                plt.bar(keys, values, color='purple')
                plt.title(f"Count Metrics - {tracker} - {seq}")
                plt.xticks(rotation=45, ha='right')
                plt.ylabel('Cantidad')
                plt.tight_layout()
                plt.show()

def main():
    archivo = 'resultado.txt'  # Cambiar por el path de tu archivo txt
    resultados = parse_motchallenge_txt(archivo)
    plot_metrics(resultados)

if __name__ == "__main__":
    main()
