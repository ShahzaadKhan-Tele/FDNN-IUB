import matplotlib.pyplot as plt
import numpy as np
import json
import os

def bandwidth_o_time_single(data):
    band_la = data.get("Bandwidth", {})

    if "wifi_bandwidth" not in band_la:
        print("Error: 'wifi_bandwidth' not found in data['Bandwidth']")
        return

    lists = ["wifi_bandwidth", "lifi_bandwidth", "hybrid_bandwidth"]
    colors = ['blue', 'orange', 'green']

    os.makedirs("Data Images", exist_ok=True)

    for i, li in enumerate(lists):
        ty = band_la.get(li, [])

        if not ty:  # Skip if no data
            print(f"Warning: No data for {li}, skipping plot.")
            continue

        time_points = np.linspace(0, 100, len(ty))  # Generate time axis

        # Plot each bandwidth separately
        plt.figure(figsize=(10, 6))
        plt.plot(time_points, ty, label=f"{li}", color=colors[i])
        plt.xlabel('Time (s)')
        plt.ylabel('Bandwidth Utilization (%)')
        plt.title(f'{li} Over Time')
        plt.legend()
        plt.grid(False)
        plt.show()  # Show the individual plot

        # Save individual plot
        file_path = os.path.join("Data Images", f"{li}.png")
        plt.savefig(file_path)
        print(f"Saved: {file_path}")
        plt.close()





def plot_mul_single(data):
    band_la = data["Bandwidth"]

    # Ensure all required keys exist
    if not all(key in band_la for key in ["wifi_bandwidth", "lifi_bandwidth", "hybrid_bandwidth"]):
        print("Error: One or more bandwidth keys are missing in data['Bandwidth']")
        return
    
    wifi_bandwidth = np.array(band_la["wifi_bandwidth"])
    lifi_bandwidth = np.array(band_la["lifi_bandwidth"])
    hybrid_bandwidth = np.array(band_la["hybrid_bandwidth"])
    
    # Find the minimum length to avoid shape mismatch
    min_length = min(len(wifi_bandwidth), len(lifi_bandwidth), len(hybrid_bandwidth))
    
    # Trim the bandwidth lists and limit time points to 0-30
    wifi_bandwidth = wifi_bandwidth[:min_length]
    lifi_bandwidth = lifi_bandwidth[:min_length]
    hybrid_bandwidth = hybrid_bandwidth[:min_length]
    
    time_points = np.linspace(0, 30, min_length)  # Limit to 0-30

    plt.figure(figsize=(10, 5))
    plt.plot(time_points, wifi_bandwidth, label="Wi-Fi Bandwidth", linestyle='-')
    plt.plot(time_points, lifi_bandwidth, label="Li-Fi Bandwidth", linestyle='--')
    plt.plot(time_points, hybrid_bandwidth, label="Hybrid Bandwidth", linestyle='-.')

    plt.xlabel("Time")
    plt.ylabel("Bandwidth")
    plt.title("Wi-Fi, Li-Fi, and Hybrid Bandwidths Over Time (0-30)")
    plt.legend()
    plt.grid(False)
    plt.show()
    plt.savefig(f"Data Images\All Bandwidths.png")
def plot_graphs(figx=None,figy=None,x_p=None,y_p=None,mul=False,mul_plot=0,plotlist=[],m_k=None,lb=None,ls=None,x=None,y=None,lengend="",grid=False,show=False,name=None,color="blue",tight=False):
    plt.figure(figsize=(figx,figy))
    labels=[]
    if mul:
        for muls in range(mul_plot):
            pol = plotlist[muls]
            plt.plot(pol["x_p"], pol["y_p"],label=pol["lb"],linestyle=pol["ls"])
            labels.append(pol["lb"],) 
    else:
        plt.plot(x_p, y_p, marker =m_k,label=lb,linestyle=ls,color=color)
        # plt.legend([lb])
        labels.append(lb)
    plt.xlabel(x)
    plt.ylabel(y)
    if lb:
        plt.legend(labels)
    else:
        plt.legend()
    plt.grid(grid)
    if show:
        plt.show()
    if name:
        plt.savefig(f"Data Images\{name}")
    if tight:
        plt.tight_layout()
    plt.close() 
def plot_user_lat_cov_snr(data):
    polts = ["user_latencies","user_covergae","user_snr","user_BER"]
    x_lables = ["Iterations","Iterations","Iterations","Iterations"]
    y_lables = ["Latencies","Coverage (%)","SNR (db)","BER"]
    polts_u = ["avg_lat_hb","avg_cov","avg_snr","avg_ber"]
    y_lables_u = ["Average Latency (MS)","Average Coverage (%)","Average SNR (db)","Average BER"]
    x_lables_u = ["users","users","Users","Users"]
    subs = ['ms','cov','db',"ber"]
    
    plot_graphs(figx=5,figy=5,x_p=np.arange(0, 5,1),y_p=data['avg_th_pt']['mbps'],x="Users",y="Average ThroughPut (MBPS)",name="Average Through Put.png",show=True,m_k="o")
    for i in range(len(polts)):
        avg = data[polts[i]]
        iteraions = np.arange(0,10,1)
        pols=[{"y_p":avg['u1'],"x_p":iteraions,"lb":"User1","ls":"-"},{"y_p":avg['u2'],"x_p":iteraions,"lb":"User2","ls":"-"},{"y_p":avg['u3'],"x_p":iteraions,"lb":"User3","ls":"-"},{"y_p":avg['u4'],"x_p":iteraions,"lb":"User4","ls":"-"},{"y_p":avg['u5'],"x_p":iteraions,"lb":"User5","ls":"-"},]
        plot_graphs(figx=10,figy=5,mul=True,mul_plot=5,plotlist=pols,x=x_lables[i],y=y_lables[i],show=True,name=polts[i])
        avg_u = data[polts_u[i]]
        ms = avg_u[subs[i]]
        num_points = len(ms) 
        users = np.arange(0, num_points,1) 
        plot_graphs(figx=10,figy=5,x_p=users,y_p=ms,m_k="o",ls="-",x=x_lables_u[i],y=y_lables_u[i],show=True,name=polts_u[i])

def latencie_overtime(data):
    time_points = np.arange(0, 100, 10)
    categories = ['wifi_latency', 'lifi_latency', 'hybrid_latency']
    colors = ['blue', 'orange', 'green']
    titles = ['Wi-Fi Latency Over Time ', 'Li-Fi Latency Over Time', 'Hybrid Latency Over Time ']
    combined_latency = data["Combined_Latency"]
    sp = data["Separate_Letancy"]
    for idx,lats in enumerate(categories):
        y=sp[lats]
        plot_graphs(figx=7,figy=5,x_p=time_points,y_p=y,x="Time (s)",y=f"{titles[idx]} (ms)",show=True,lb=categories[idx],color=colors[idx],m_k="o",name=titles[idx])
    for idx,category in enumerate(categories):
        plt.plot(
            time_points, 
            combined_latency[category], 
            label=category.replace('_', ' ').title(), 
            marker='o', 
            color=colors[idx]
        )
    plt.xlabel('Time (s)')
    plt.ylabel('Latency (ms)')
    plt.title('Latency Over Time for Wi-Fi, Li-Fi, and Hybrid Technologies')
    plt.legend()
    plt.tight_layout()
#     combined_file = "Combined_Latency.png"
def calculate_latency(network_type="Wi-Fi", speed_mbps=20):
    num_packets = 10
    distances = np.random.uniform(1, 50, size=num_packets)

    speed_of_light_air = 3e8  
    speed_of_light_fiber = 2.99e8
    
    if network_type == "Wi-Fi":
        latency_values = (distances / speed_of_light_air) * 1e6 
    elif network_type == "Li-Fi":
        latency_values = (distances / speed_of_light_fiber) * 1e6  
    elif network_type == "Hybrid":
        latency_values = (distances / ((speed_of_light_air + speed_of_light_fiber) / 2)) * 1e6  
    else:
        raise ValueError("Invalid network type. Choose 'Wi-Fi', 'Li-Fi', or 'Hybrid'.")
    
    return latency_values

# def latencie_overtime(network_type,c="b"):
#     latencies = calculate_latency(network_type, 20)
#     plt.figure(figsize=(8, 5))
#     plt.plot(range(1, 11), latencies, linestyle='-', label=f'{network_type} Latency', color=c)
#     plt.xlabel('Packet Number')
#     plt.ylabel('Latency (µs)')
#     plt.title(f'Latency for {network_type}')
#     plt.legend()
#     plt.grid(False)
#     plt.show()
#     plt.show()
if __name__ == "__main__":
    print("Checking For Latencies:\n")
    with open("observations.json", "r") as file:
        data = json.load(file)
    print("Data of Latencies")
    latencie_overtime(data)
    # latencie_overtime("Wi-Fi",c="b")
    # latencie_overtime("Li-Fi",c="g")
    # latencie_overtime("Hybrid",c="r")
    # exit()
    print("Data of Wifi Lifi hybrid Bandwidth Function")
    print("Data of Wifi Bandwidth Function")
    
    bandwidth_o_time_single(data)
    plot_mul_single(data)
    plot_user_lat_cov_snr(data)
    