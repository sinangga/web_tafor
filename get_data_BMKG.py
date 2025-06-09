import requests
import statistics
from datetime import datetime

# Status to icon mapping for display
status_to_icon = {
    'Cerah': 'https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/cerah-am.png',
    'Hujan Ringan': 'https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/hujan%20ringan-am.png',
    'Hujan Petir': 'https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/hujan%20petir-am.png',
    'Petir': 'https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/hujan%20petir-am.png',
    'Cerah Berawan': 'https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/cerah%20berawan-am.png',
    'Hujan Lebat': 'https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/hujan%20lebat-am.png',
    'Hujan Sedang': 'https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/hujan%20sedang-am.png',
    'Kabut/Asap': 'https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/kabut-am.png',
    'Udara Kabur': 'https://raw.githubusercontent.com/sinangga/web_tafor/refs/heads/main/icon/udara%20kabur.png',
    'Berawan': 'https://api-apps.bmkg.go.id/storage/icon/cuaca/berawan-am.svg'
}

def fetch_bmkg_data():
    suffixes2_16 = [f"{i:02d}.2001" for i in range(2, 17)]
    suffixes18_23 = [f"{i:02d}.2001" for i in range(18, 24)]
    base_url = "https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4=61.06."

    urls = [
        "https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4=61.06.01.1001",
        *[base_url + suffix for suffix in suffixes2_16],
        "https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4=61.06.17.1001",
        *[base_url + suffix for suffix in suffixes18_23]
    ]

    df_kh = [requests.get(url).json() for url in urls]
    return df_kh

def process_bmkg_data(df_kh):
    list_kecamatan = [item['lokasi']['kecamatan'] for item in df_kh]
    df_kh_2 = dict(zip(list_kecamatan, df_kh))

    def nesting(nama_kecamatan):
        cuaca_data = df_kh_2[nama_kecamatan]['data'][0]['cuaca']
        all_entries = [entry for group in cuaca_data[:3] for entry in group]
        all_entries.sort(key=lambda x: x['local_datetime'])
        return all_entries

    def cuaca_pertama(n):
        data = nesting(n)
        suhu = [d["t"] for d in data[:8]]
        rh = [d["hu"] for d in data[:8]]
        arah = [d["wd"] for d in data[:8]]
        angin = [d["ws"] for d in data[:8]]
        list_cuaca = [d["weather_desc"] for d in data[:8]]
        waktu = [d["local_datetime"] for d in data[:8]]
        
        # ⏰ Get actual hours from BMKG local_datetime
        hours = [str(datetime.strptime(t, "%Y-%m-%d %H:%M:%S").hour).zfill(2) for t in waktu]
        
        return n, waktu, list_cuaca, f"{min(suhu)}-{max(suhu)}", f"{min(rh)}-{max(rh)}", statistics.mode(arah), max(angin), hours

    def harian_kecamatan(waktu_func, nama):
        result = waktu_func(nama)
        (a, waktu, cuaca_list, suhu, rh, arah, angin, hours) = result
        
        # Rearrange the row
        row = [a] + cuaca_list + [suhu + "°C", rh + "%", arah, f"{round(angin)} Knot"]
        return row

    # Get dynamic hours from one sample
    _, waktu_sample, _, _, _, _, _, hours = cuaca_pertama(list_kecamatan[0])
    jam = ['KECAMATAN'] + hours + ['SUHU', 'KELEMBAPAN', 'ANGIN', 'KECEPATAN']
    result_dicts = [dict(zip(jam, harian_kecamatan(cuaca_pertama, kec))) for kec in list_kecamatan]
    return result_dicts, jam, status_to_icon
