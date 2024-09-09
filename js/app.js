var local_path = '/output_file.json'

d3.json(local_path).then(function (data) {
  //just logging data 
  console.log(data);

  // Step 1: Group data by 'Release_year', create a function to checking if the year key exists in the accumulate object. 
  //If it doesn’t, initialise an empty array. Then adds the current game object to the array.
  function groupByYear (accumulator, current) {

    const year = current.Release_year;

    if(!accumulator[year]) {
      accumulator[year] = [];
    };

    accumulator[year].push(current);

    return accumulator;
  };
  

  const groupedData = data.reduce(groupByYear, {});

  // Step 2: Sort each group by 'Peak_CCU' in descending order
  for (const year in groupedData) {
    groupedData[year].sort((a, b) => b.Peak_CCU - a.Peak_CCU);
  };

  // Step 3: Select the top 10 games per year
  const topGamesPerYear = {};
  for (const year in groupedData) {
    topGamesPerYear[year] = groupedData[year].slice(0,10);
  };

  console.log(topGamesPerYear);

  // Append the year into dropdown 
  let dropdown = d3.select("#year-dropdown");
  const years = Object.keys(groupedData).sort();

  // Append the years as options in the dropdown menu
  years.forEach(year => {
    dropdown.append('option').text(year).property('value', year);
  });

  //show the default year 
  const defaultYear =  years[0];

  // Plot the bar chart for the default year
  plotBarChart(topGamesPerYear[defaultYear]);
 
  // Function to plot the bar chart
  function plotBarChart(data) {
    let barNames = data.map(obj => obj.Name);
    let barValues = data.map(obj => obj.Peak_CCU);
    let barLabel = data.map(obj => `Metacritic score: ${obj.Metacritic_score}`);

    let trace1 = {
      x: barNames,
      y: barValues,
      type: 'bar',
      text: barLabel,
      //textposition: 'horizontal',
      marker: {
        color: barValues,
        colorscale: "Viridis"
      }
    };

    let barData = [trace1];

    let layout = {
      title: 'Top 10 Games by Peak CCU per Year',
      xaxis: {
          title: 'Games',
          automargin: true
      },
      yaxis: {
          title: 'Peak CCU',
          automargin: true
      },
      margin: {
          l: 50, // left margin
          r: 50, // right margin
          b: 100, // bottom margin to create space for x-axis labels
          t: 50 // top margin
      },
      hovermode: 'closest'
  };
  
    Plotly.newPlot('bar', barData, layout);
  };

  function displayPanelInfo (data) {
    const topGame = data[0].Name;
    const avgMetacriticScore = d3.mean(data, d => d.Metacritic_score);
    const developers = data.map(d => d.Developers).flat();
    const publishers = data.map(d => d.Publishers).flat();

    const topDeveloper = d3.max(developers, d => d);
    const topPublisher = d3.max(publishers, d => d);
    const genres = data.map(d => d.Genres).flat();
    const uniqueGenres = [...new Set(genres)];  // Get unique genres
    const popularGenres = uniqueGenres.join(', ');  // Convert to comma-separated string
    
    d3.select("#sample-metadata").html(`
      <p><strong>Top Game:</strong> ${topGame}</p>
      <p><strong>Average Metacritic Score:</strong> ${avgMetacriticScore.toFixed(2)}</p>
      <p><strong>Top Developer(s):</strong> ${topDeveloper}</p>
      <p><strong>Top Publisher(s):</strong> ${topPublisher}</p>
      <p><strong>Popular Genre(s):</strong> ${popularGenres}</p>
    `);
  };

  //Update the bar chart when the dropdown selection changes
  dropdown.on('change', function () {
    const selectedYear = dropdown.property('value');
    plotBarChart(topGamesPerYear[selectedYear]);
    displayPanelInfo(topGamesPerYear[selectedYear]);
  });

}).catch(function (error) {
  console.error('Error loading the JSON data:', error);
});