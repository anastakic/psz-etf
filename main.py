from task_1_data_collecting import DataCollector
from task_2_data_analysis import DataAnalysis
from task_3_data_visualization import DataVisualization


def main():
    data_collector = DataCollector()
    data_collector.start()
    data_analysis = DataAnalysis()
    data_analysis.do_analysis()
    data_visualization = DataVisualization()
    data_visualization.do_visualization()


if __name__ == '__main__':
    main()
