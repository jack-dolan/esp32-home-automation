import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const TemperatureChart: React.FC = () => {
  // Mock data - this would come from your API in a real implementation
  const data = {
    labels: ['8AM', '9AM', '10AM', '11AM', '12PM', '1PM', '2PM'],
    datasets: [
      {
        label: 'Living Room',
        data: [22, 22.5, 23, 23.5, 24, 23.5, 23],
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
      {
        label: 'Bedroom',
        data: [21, 21.5, 22, 22.5, 23, 22.5, 22],
        borderColor: 'rgb(53, 162, 235)',
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Temperature Over Time',
      },
    },
  };

  return (
    <div className="temperature-chart">
      <Line data={data} options={options} />
    </div>
  );
};

export default TemperatureChart;