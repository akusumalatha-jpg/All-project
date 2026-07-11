"""
Metrics Module
Extracts and calculates KPIs from Excel data.
"""

from typing import List, Dict, Any, Union
import statistics
import logging

logger = logging.getLogger(__name__)


class MetricsCalculator:
    """Calculates KPIs from data."""

    def __init__(self):
        """Initialize metrics calculator."""
        self.kpis = {}

    def sum_column(self, data: List[Dict], column_name: str, label: str = None) -> Dict:
        """
        Sum values in a column.
        
        Args:
            data: List of dictionaries
            column_name: Column to sum
            label: Custom label for KPI
            
        Returns:
            KPI dictionary with name, value, type
        """
        try:
            if not data:
                logger.warning(f"No data to sum for column: {column_name}")
                return None

            values = [
                float(row[column_name]) for row in data
                if column_name in row and row[column_name] is not None
            ]

            if not values:
                logger.warning(f"No numeric values found in column: {column_name}")
                return None

            total = sum(values)
            kpi = {
                'name': label or f"Total {column_name}",
                'value': round(total, 2),
                'type': 'sum',
                'count': len(values)
            }
            logger.info(f"Calculated sum for {column_name}: {total}")
            return kpi

        except Exception as e:
            logger.error(f"Error calculating sum: {str(e)}")
            return None

    def average_column(self, data: List[Dict], column_name: str, label: str = None) -> Dict:
        """
        Calculate average of column values.
        
        Args:
            data: List of dictionaries
            column_name: Column to average
            label: Custom label for KPI
            
        Returns:
            KPI dictionary
        """
        try:
            if not data:
                return None

            values = [
                float(row[column_name]) for row in data
                if column_name in row and row[column_name] is not None
            ]

            if not values:
                return None

            avg = statistics.mean(values)
            kpi = {
                'name': label or f"Average {column_name}",
                'value': round(avg, 2),
                'type': 'average',
                'count': len(values)
            }
            logger.info(f"Calculated average for {column_name}: {avg}")
            return kpi

        except Exception as e:
            logger.error(f"Error calculating average: {str(e)}")
            return None

    def count_rows(self, data: List[Dict], label: str = None) -> Dict:
        """
        Count total rows.
        
        Args:
            data: List of dictionaries
            label: Custom label
            
        Returns:
            KPI dictionary
        """
        if not data:
            return None

        count = len(data)
        kpi = {
            'name': label or "Total Records",
            'value': count,
            'type': 'count'
        }
        logger.info(f"Counted {count} records")
        return kpi

    def count_unique(self, data: List[Dict], column_name: str, label: str = None) -> Dict:
        """
        Count unique values in column.
        
        Args:
            data: List of dictionaries
            column_name: Column to count unique values
            label: Custom label
            
        Returns:
            KPI dictionary
        """
        try:
            if not data:
                return None

            unique_values = set()
            for row in data:
                if column_name in row and row[column_name] is not None:
                    unique_values.add(str(row[column_name]))

            count = len(unique_values)
            kpi = {
                'name': label or f"Unique {column_name}",
                'value': count,
                'type': 'unique_count',
                'values': sorted(list(unique_values))
            }
            logger.info(f"Counted {count} unique values in {column_name}")
            return kpi

        except Exception as e:
            logger.error(f"Error counting unique values: {str(e)}")
            return None

    def group_by(self, data: List[Dict], group_column: str, 
                 aggregate_column: str = None, agg_type: str = 'sum') -> Dict:
        """
        Group data by column and aggregate.
        
        Args:
            data: List of dictionaries
            group_column: Column to group by
            aggregate_column: Column to aggregate (if None, count only)
            agg_type: Aggregation type ('sum', 'average', 'count')
            
        Returns:
            Dictionary with grouped data
        """
        try:
            if not data:
                return None

            grouped = {}

            for row in data:
                if group_column not in row:
                    continue

                key = str(row[group_column])
                if key not in grouped:
                    grouped[key] = {'count': 0, 'values': []}

                grouped[key]['count'] += 1

                if aggregate_column and aggregate_column in row and row[aggregate_column] is not None:
                    try:
                        grouped[key]['values'].append(float(row[aggregate_column]))
                    except (ValueError, TypeError):
                        pass

            result = {'name': f"{group_column} Groups", 'groups': {}}

            for key in sorted(grouped.keys()):
                group_data = grouped[key]
                group_result = {'count': group_data['count']}

                if aggregate_column and group_data['values']:
                    if agg_type == 'sum':
                        group_result['aggregate'] = round(sum(group_data['values']), 2)
                    elif agg_type == 'average':
                        group_result['aggregate'] = round(statistics.mean(group_data['values']), 2)
                    group_result['aggregate_type'] = agg_type

                result['groups'][key] = group_result

            logger.info(f"Grouped {len(data)} rows by {group_column}")
            return result

        except Exception as e:
            logger.error(f"Error grouping data: {str(e)}")
            return None

    def percentile(self, data: List[Dict], column_name: str, 
                   percentile: float = 50, label: str = None) -> Dict:
        """
        Calculate percentile of column.
        
        Args:
            data: List of dictionaries
            column_name: Column to calculate percentile
            percentile: Percentile value (0-100, default 50 for median)
            label: Custom label
            
        Returns:
            KPI dictionary
        """
        try:
            if not data:
                return None

            values = sorted([
                float(row[column_name]) for row in data
                if column_name in row and row[column_name] is not None
            ])

            if not values:
                return None

            k = (len(values) - 1) * percentile / 100
            f = int(k)
            c = k - f

            if f + 1 < len(values):
                value = values[f] * (1 - c) + values[f + 1] * c
            else:
                value = values[f]

            kpi = {
                'name': label or f"{percentile}th Percentile {column_name}",
                'value': round(value, 2),
                'type': 'percentile',
                'percentile': percentile
            }
            logger.info(f"Calculated {percentile}th percentile: {value}")
            return kpi

        except Exception as e:
            logger.error(f"Error calculating percentile: {str(e)}")
            return None

    def min_max(self, data: List[Dict], column_name: str) -> Dict:
        """
        Find min and max values.
        
        Args:
            data: List of dictionaries
            column_name: Column to find min/max
            
        Returns:
            Dictionary with min and max
        """
        try:
            if not data:
                return None

            values = [
                float(row[column_name]) for row in data
                if column_name in row and row[column_name] is not None
            ]

            if not values:
                return None

            result = {
                'name': f"Min/Max {column_name}",
                'min': round(min(values), 2),
                'max': round(max(values), 2),
                'range': round(max(values) - min(values), 2),
                'type': 'min_max'
            }
            logger.info(f"Min: {result['min']}, Max: {result['max']}")
            return result

        except Exception as e:
            logger.error(f"Error calculating min/max: {str(e)}")
            return None

    def create_summary(self, data: List[Dict], metrics: List[Dict]) -> Dict:
        """
        Create summary report with multiple KPIs.
        
        Args:
            data: Source data
            metrics: List of metric configurations
            
        Returns:
            Dictionary with all calculated KPIs
        """
        summary = {
            'total_records': len(data),
            'kpis': {}
        }

        for metric in metrics:
            try:
                metric_type = metric.get('type')
                column = metric.get('column')
                label = metric.get('label', column)

                if metric_type == 'sum':
                    kpi = self.sum_column(data, column, label)
                elif metric_type == 'average':
                    kpi = self.average_column(data, column, label)
                elif metric_type == 'count':
                    kpi = self.count_rows(data, label)
                elif metric_type == 'unique':
                    kpi = self.count_unique(data, column, label)
                elif metric_type == 'group':
                    kpi = self.group_by(data, column, metric.get('aggregate_column'))
                else:
                    logger.warning(f"Unknown metric type: {metric_type}")
                    continue

                if kpi:
                    summary['kpis'][label] = kpi

            except Exception as e:
                logger.error(f"Error processing metric {metric}: {str(e)}")

        logger.info(f"Created summary with {len(summary['kpis'])} KPIs")
        return summary
