function processData(tasks) {
    const groupedData = {};
    const labels = Array.from({ length: 24 }, (_, i) => i.toString().padStart(2, '0') + ':00');

    for (const task of tasks) {
        const hour = luxon.DateTime.fromISO(task.date).hour;
        const taskName = task.name__name;

        if (!groupedData[taskName]) {
            groupedData[taskName] = Array(24).fill(0);
        }

        groupedData[taskName][hour] += task.length / 60;  // convert to hours
    }

    const datasets = Object.entries(groupedData).map(([label, data], i, arr) => ({
        label,
        data,
        borderColor: pickColor(i, arr.length),
        fill: false
    }));

    return { labels, datasets };
}
