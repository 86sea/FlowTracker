if (ongoingTaskData) {
    console.log(ongoingTaskData);
    const startDate = new Date(ongoingTaskData.date);
    const taskLengthMinutes = ongoingTaskData.length;
    const taskName = ongoingTaskData.name;
    const endDate = new Date(startDate.getTime() + taskLengthMinutes * 60 * 1000); // Add task length (in ms) to the start time
    var totalDuration = taskLengthMinutes * 60 * 1000;  // Total task duration in milliseconds
    
    // Update progress bar value

    var countdown = setInterval(function() {
        var now = new Date().getTime();
        var elapsedTime = now - startDate.getTime();  // Time elapsed since the task started
        var remainingTime = totalDuration - elapsedTime;  // Remaining time in milliseconds
        var remainingPercentage = (remainingTime / totalDuration) * 100;  // Remaining time as a percentage of total duration
        document.getElementById("timer").style.setProperty('--value', remainingPercentage.toFixed(0));
        var distance = endDate - now;



        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        document.getElementById("timer").innerHTML =
        + minutes + ":" + seconds + "<br>" + taskName;

        if (distance < 0) {
            clearInterval(countdown);
            document.getElementById("timer").innerHTML = "Task has ended";
        if (Notification.permission === "granted") {
                new Notification('Timer Ended!', {
                    body: 'Your task "' + taskName + '" has ended!',
                });
            }
        }
    }, 1000);
} else {
    console.log('There is no ongoing task');
}
