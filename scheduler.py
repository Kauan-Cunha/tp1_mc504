import csv
import sys
import heapq

def read_processes(filename):
    """Read processes from a CSV file."""

    processes = []

    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            processes.append({
                "name": row["nome"],
                "burst": int(row["burst"]),
                "arrival": int(row["chegada"]),
                "priority": int(row["prioridade"]),
            })

    return processes


# ---------------------------------------------------------------------------
# Scheduling algorithms
# ---------------------------------------------------------------------------

def fcfs(processes):
    """
    First-Come, First-Served.

    Returns:
        events: list of (time, process_name)
        average_waiting_time: float
    """
    if not processes:
        return [], 0.0

    res = []
    espera, t = 0, 0

    for p in processes:
        #piddle handler
        if p['arrival'] > t:
            res.append((t, 'Pidle'))
            t = p['arrival']

        res.append((t, p['name']))
        espera += t - p['arrival']
        t += p['burst']

    return res, espera/len(processes)


def sjf(processes):
    """
    Shortest-Job-First (non-preemptive).

    Returns:
        events: list of (time, process_name)
        average_waiting_time: float
    """
    if not processes:
        return [], 0.0

    res, heap = [],[] 
    espera, t = 0, processes[0]['arrival']
    if t > 0: res.append((0, 'Pidle'))

    i, n = 0, len(processes)
    while i < n or heap:

        #adiciona todos os processos que já chegaram em um heap
        while i < n and processes[i]['arrival'] <= t:
            p = processes[i]
            heapq.heappush(heap, (p['burst'], i, p['name'], p['arrival']))
            i += 1


        if not heap:
            res.append((t, 'Pidle'))
            t = processes[i]['arrival']
            continue

        burst, _, name, arrival = heapq.heappop(heap)

        res.append((t, name))
        espera += t - arrival
        t += burst

    return res, espera/n

def srtf(processes):
    """
    Shortest-Remaining-Time-First (preemptive).

    Returns:
        events: list of (time, process_name)
        average_waiting_time: float
    """

    # TODO: implement
    return [], 0.0


def round_robin(processes, quantum):
    """
    Round-Robin.

    Returns:
        events: list of (time, process_name)
        average_waiting_time: float
    """

    # TODO: implement
    return [], 0.0


def priority(processes):
    """
    Priority scheduling (non-preemptive).

    Lower numerical value means higher priority.

    Returns:
        events: list of (time, process_name)
        average_waiting_time: float
    """

    # TODO: implement
    return [], 0.0


def priority_preemptive(processes):
    """
    Priority scheduling (preemptive).

    Lower numerical value means higher priority.

    Returns:
        events: list of (time, process_name)
        average_waiting_time: float
    """

    # TODO: implement
    return [], 0.0


def priority_rr(processes, quantum):
    """
    Priority scheduling with Round-Robin among processes
    with the same priority.

    Lower numerical value means higher priority.

    Returns:
        events: list of (time, process_name)
        average_waiting_time: float
    """

    # TODO: implement
    return [], 0.0


# ---------------------------------------------------------------------------
# Command-line interface
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 3:
        print(
            "Uso: python scheduler.py <arquivo.csv> <algoritmo> [quantum]"
        )
        sys.exit(1)

    filename = sys.argv[1]
    algorithm = sys.argv[2].lower()

    processes = read_processes(filename)

    if algorithm == "fcfs":
        events, average_waiting_time = fcfs(processes)

    elif algorithm == "sjf":
        events, average_waiting_time = sjf(processes)

    elif algorithm == "srtf":
        events, average_waiting_time = srtf(processes)

    elif algorithm == "rr":
        if len(sys.argv) != 4:
            print("Erro: o Round-Robin exige um quantum.")
            sys.exit(1)

        quantum = int(sys.argv[3])
        events, average_waiting_time = round_robin(
            processes, quantum
        )

    elif algorithm == "priority":
        events, average_waiting_time = priority(processes)

    elif algorithm == "priority-preemptive":
        events, average_waiting_time = priority_preemptive(processes)

    elif algorithm == "priority-rr":
        if len(sys.argv) != 4:
            print("Erro: o Priority-RR exige um quantum.")
            sys.exit(1)

        quantum = int(sys.argv[3])
        events, average_waiting_time = priority_rr(
            processes, quantum
        )

    else:
        print(f"Algoritmo desconhecido: {algorithm}")
        sys.exit(1)

    print(f"Tempo médio de espera: {average_waiting_time:.2f}")
    print("t  Processo")

    for time, process_name in events:
        print(f"{time:<3}{process_name}")


if __name__ == "__main__":
    main()