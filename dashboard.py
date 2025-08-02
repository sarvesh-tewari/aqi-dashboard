#!/usr/bin/env python3
"""
Interactive AQI Dashboard using Streamlit
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, date
import json

# Page configuration
st.set_page_config(
    page_title="AQI Dashboard - India Air Quality Analysis",
    page_icon="🌬️",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    """Load the processed AQI data"""
    try:
        df = pd.read_parquet("data/processed/aqi_data.parquet")
        
        # Convert date column to datetime if it's not already
        if not pd.api.types.is_datetime64_any_dtype(df['date']):
            df['date'] = pd.to_datetime(df['date'])
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

@st.cache_data
def load_summary():
    """Load the data summary"""
    try:
        with open("data/processed/aqi_summary.json", "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading summary: {e}")
        return {}

def create_header():
    """Create the dashboard header"""
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h1>🌬️ AQI Dashboard - India Air Quality Analysis</h1>
        <p style="font-size: 1.2rem; color: #666;">
            Comprehensive Air Quality Index analysis for Lucknow, Mysuru, Delhi, and Dehradun (2017-2025)
        </p>
    </div>
    """, unsafe_allow_html=True)

def create_sidebar():
    """Create the sidebar with filters"""
    st.sidebar.markdown("## 📊 Dashboard Controls")
    
    # Load data
    df = load_data()
    if df.empty:
        return {}, {}
    
    # City filter
    cities = sorted(df['city'].unique())
    selected_cities = st.sidebar.multiselect(
        "🏙️ Select Cities",
        cities,
        default=cities,
        help="Choose cities to analyze"
    )
    
    # Year filter
    years = sorted(df['year'].unique())
    selected_years = st.sidebar.multiselect(
        "📅 Select Years",
        years,
        default=years,
        help="Choose years to analyze"
    )
    
    # Date range filter
    if not df.empty:
        min_date = df['date'].min()
        max_date = df['date'].max()
        
        date_range = st.sidebar.date_input(
            "📆 Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            help="Select date range for analysis"
        )
    
    # AQI range filter
    if not df.empty:
        available_data = df[df['data_quality'] == 'available']
        min_aqi = int(available_data['aqi_value'].min())
        max_aqi = int(available_data['aqi_value'].max())
        
        aqi_range = st.sidebar.slider(
            "📈 AQI Range",
            min_value=min_aqi,
            max_value=max_aqi,
            value=(min_aqi, max_aqi),
            help="Filter data by AQI value range"
        )
    
    return selected_cities, selected_years, date_range, aqi_range

def filter_data(df, cities, years, date_range, aqi_range):
    """Filter data based on sidebar selections"""
    if df.empty:
        return df
    
    # Filter by cities
    if cities:
        df = df[df['city'].isin(cities)]
    
    # Filter by years
    if years:
        df = df[df['year'].isin(years)]
    
    # Filter by date range
    if len(date_range) == 2:
        start_date, end_date = date_range
        df = df[(df['date'] >= pd.to_datetime(start_date)) & 
                (df['date'] <= pd.to_datetime(end_date))]
    
    # Filter by AQI range
    if len(aqi_range) == 2:
        min_aqi, max_aqi = aqi_range
        available_data = df[df['data_quality'] == 'available']
        available_data = available_data[
            (available_data['aqi_value'] >= min_aqi) & 
            (available_data['aqi_value'] <= max_aqi)
        ]
        missing_data = df[df['data_quality'] == 'missing']
        df = pd.concat([available_data, missing_data])
    
    return df

def calculate_city_metrics(df):
    """Calculate city-specific AQI metrics"""
    if df.empty:
        return pd.DataFrame()
    
    # Filter for available data only
    available_data = df[df['data_quality'] == 'available']
    
    if available_data.empty:
        return pd.DataFrame()
    
    # Calculate metrics by city and year
    metrics = []
    
    for city in available_data['city'].unique():
        city_data = available_data[available_data['city'] == city]
        
        for year in city_data['year'].unique():
            year_data = city_data[city_data['year'] == year]
            
            # Calculate metrics
            days_above_100 = len(year_data[year_data['aqi_value'] > 100])
            days_below_50 = len(year_data[year_data['aqi_value'] < 50])
            peak_aqi = year_data['aqi_value'].max()
            avg_aqi = year_data['aqi_value'].mean()
            median_aqi = year_data['aqi_value'].median()
            total_days = len(year_data)
            
            metrics.append({
                'city': city,
                'year': year,
                'days_above_100': days_above_100,
                'days_below_50': days_below_50,
                'peak_aqi': peak_aqi,
                'avg_aqi': avg_aqi,
                'median_aqi': median_aqi,
                'total_days': total_days,
                'percentage_above_100': (days_above_100 / total_days * 100) if total_days > 0 else 0,
                'percentage_below_50': (days_below_50 / total_days * 100) if total_days > 0 else 0
            })
    
    return pd.DataFrame(metrics)

def create_city_metrics_section(df):
    """Create city-specific metrics section"""
    st.markdown("## 📊 City-Specific AQI Metrics")
    
    if df.empty:
        st.warning("No data available for the selected filters.")
        return
    
    # Calculate metrics
    metrics_df = calculate_city_metrics(df)
    
    if metrics_df.empty:
        st.warning("No available data for the selected filters.")
        return
    
    # Display metrics by city
    for city in metrics_df['city'].unique():
        city_metrics = metrics_df[metrics_df['city'] == city]
        
        st.markdown(f"### 🏙️ {city}")
        
        # Create metrics display
        cols = st.columns(4)
        
        with cols[0]:
            total_days = city_metrics['total_days'].sum()
            st.metric(
                "📅 Total Days",
                f"{total_days:,}",
                help=f"Total days with AQI data for {city}"
            )
        
        with cols[1]:
            avg_peak = city_metrics['peak_aqi'].mean()
            st.metric(
                "🔥 Average Peak AQI",
                f"{avg_peak:.0f}",
                help=f"Average peak AQI across all years for {city}"
            )
        
        with cols[2]:
            avg_median = city_metrics['median_aqi'].mean()
            st.metric(
                "📊 Average Median AQI",
                f"{avg_median:.0f}",
                help=f"Average median AQI across all years for {city}"
            )
        
        with cols[3]:
            total_above_100 = city_metrics['days_above_100'].sum()
            st.metric(
                "⚠️ Days Above 100",
                f"{total_above_100:,}",
                f"{total_above_100/total_days*100:.1f}%" if total_days > 0 else "0%",
                help=f"Days with AQI > 100 (unhealthy) for {city}"
            )
        
        # Add a new row for additional metrics
        cols2 = st.columns(4)
        
        with cols2[0]:
            total_below_50 = city_metrics['days_below_50'].sum()
            st.metric(
                "✅ Days Below 50",
                f"{total_below_50:,}",
                f"{total_below_50/total_days*100:.1f}%" if total_days > 0 else "0%",
                help=f"Days with AQI < 50 (good) for {city}"
            )
        
        # Show year-wise breakdown
        st.markdown("#### 📈 Year-wise Breakdown")
        
        # Create a table for year-wise metrics
        display_df = city_metrics[['year', 'total_days', 'days_above_100', 'days_below_50', 
                                 'peak_aqi', 'avg_aqi', 'median_aqi', 'percentage_above_100', 'percentage_below_50']].copy()
        display_df = display_df.sort_values('year')
        
        # Format the display
        display_df['peak_aqi'] = display_df['peak_aqi'].round(0).astype(int)
        display_df['avg_aqi'] = display_df['avg_aqi'].round(1)
        display_df['median_aqi'] = display_df['median_aqi'].round(1)
        display_df['percentage_above_100'] = display_df['percentage_above_100'].round(1)
        display_df['percentage_below_50'] = display_df['percentage_below_50'].round(1)
        
        # Rename columns for display
        display_df.columns = ['Year', 'Total Days', 'Days > 100', 'Days < 50', 
                             'Peak AQI', 'Avg AQI', 'Median AQI', '% > 100', '% < 50']
        
        st.dataframe(display_df, use_container_width=True)
        st.markdown("---")

def create_time_series_chart(df):
    """Create time series chart"""
    st.markdown("## 📈 Time Series Analysis")
    
    if df.empty:
        st.warning("No data available for the selected filters.")
        return
    
    # Filter for available data only
    available_data = df[df['data_quality'] == 'available'].copy()
    
    if available_data.empty:
        st.warning("No available data for the selected filters.")
        return
    
    # Create time series chart
    fig = px.line(
        available_data,
        x='date',
        y='aqi_value',
        color='city',
        title='AQI Trends Over Time',
        labels={'aqi_value': 'AQI Value', 'date': 'Date', 'city': 'City'},
        hover_data=['year', 'month', 'day']
    )
    
    # Add AQI category lines
    fig.add_hline(y=50, line_dash="dash", line_color="green", 
                  annotation_text="Good (0-50)", annotation_position="right")
    fig.add_hline(y=100, line_dash="dash", line_color="yellow", 
                  annotation_text="Moderate (51-100)", annotation_position="right")
    fig.add_hline(y=150, line_dash="dash", line_color="orange", 
                  annotation_text="Unhealthy for Sensitive Groups (101-150)", annotation_position="right")
    fig.add_hline(y=200, line_dash="dash", line_color="red", 
                  annotation_text="Unhealthy (151-200)", annotation_position="right")
    fig.add_hline(y=300, line_dash="dash", line_color="purple", 
                  annotation_text="Very Unhealthy (201-300)", annotation_position="right")
    
    fig.update_layout(
        height=500,
        xaxis_title="Date",
        yaxis_title="AQI Value",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_city_comparison_chart(df):
    """Create city comparison chart"""
    st.markdown("## 🏙️ City Comparison")
    
    if df.empty:
        st.warning("No data available for the selected filters.")
        return
    
    # Filter for available data only
    available_data = df[df['data_quality'] == 'available']
    
    if available_data.empty:
        st.warning("No available data for the selected filters.")
        return
    
    # Create comparison chart
    col1, col2 = st.columns(2)
    
    with col1:
        # Box plot for AQI distribution
        fig_box = px.box(
            available_data,
            x='city',
            y='aqi_value',
            title='AQI Distribution by City',
            labels={'aqi_value': 'AQI Value', 'city': 'City'}
        )
        fig_box.update_layout(height=400)
        st.plotly_chart(fig_box, use_container_width=True)
    
    with col2:
        # Bar chart for average AQI
        avg_aqi_by_city = available_data.groupby('city')['aqi_value'].agg(['mean', 'std', 'count']).reset_index()
        
        fig_bar = px.bar(
            avg_aqi_by_city,
            x='city',
            y='mean',
            title='Average AQI by City',
            labels={'mean': 'Average AQI', 'city': 'City'},
            error_y='std'
        )
        fig_bar.update_layout(height=400)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Add median AQI comparison
    col3, col4 = st.columns(2)
    
    with col3:
        # Bar chart for median AQI
        median_aqi_by_city = available_data.groupby('city')['aqi_value'].agg(['median', 'count']).reset_index()
        
        fig_median = px.bar(
            median_aqi_by_city,
            x='city',
            y='median',
            title='Median AQI by City',
            labels={'median': 'Median AQI', 'city': 'City'}
        )
        fig_median.update_layout(height=400)
        st.plotly_chart(fig_median, use_container_width=True)
    
    with col4:
        # Comparison chart: Average vs Median
        comparison_data = available_data.groupby('city')['aqi_value'].agg(['mean', 'median']).reset_index()
        comparison_data = comparison_data.melt(id_vars=['city'], 
                                             value_vars=['mean', 'median'],
                                             var_name='metric', 
                                             value_name='aqi_value')
        comparison_data['metric'] = comparison_data['metric'].map({'mean': 'Average', 'median': 'Median'})
        
        fig_comparison = px.bar(
            comparison_data,
            x='city',
            y='aqi_value',
            color='metric',
            title='Average vs Median AQI by City',
            labels={'aqi_value': 'AQI Value', 'city': 'City', 'metric': 'Metric'},
            barmode='group'
        )
        fig_comparison.update_layout(height=400)
        st.plotly_chart(fig_comparison, use_container_width=True)

def create_monthly_analysis(df):
    """Create monthly analysis chart"""
    import numpy as np
    import plotly.graph_objects as go
    
    st.markdown("## 📅 Monthly Analysis")
    
    if df.empty:
        st.warning("No data available for the selected filters.")
        return
    
    # Filter for available data only
    available_data = df[df['data_quality'] == 'available']
    
    if available_data.empty:
        st.warning("No available data for the selected filters.")
        return
    
    # Add year filter for heatmap
    years = sorted(available_data['year'].unique())
    selected_heatmap_year = st.selectbox(
        "📅 Select Year for Heatmap",
        ['All Years'] + list(years),
        key="heatmap_year_selector",
        help="Choose specific year or view all years combined"
    )
    
    # Filter data based on year selection
    if selected_heatmap_year == 'All Years':
        heatmap_data = available_data
    else:
        heatmap_data = available_data[available_data['year'] == selected_heatmap_year]
    
    # Create monthly heatmap for average AQI
    monthly_data = heatmap_data.groupby(['city', 'month'])['aqi_value'].mean().reset_index()
    monthly_data['metric'] = 'Average'
    
    # Create monthly heatmap for median AQI
    monthly_median_data = heatmap_data.groupby(['city', 'month'])['aqi_value'].median().reset_index()
    monthly_median_data['metric'] = 'Median'
    
    # Combine average and median data
    monthly_data = pd.concat([monthly_data, monthly_median_data], ignore_index=True)
    
    # Map numeric months to month names
    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    
    # Convert numeric months to month names
    monthly_data['month_name'] = monthly_data['month'].map(month_names)
    
    # Create month order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    
    # Add metric selector for heatmap
    metric_selector = st.selectbox(
        "📊 Select Metric for Heatmap",
        ['Average', 'Median'],
        key="metric_selector",
        help="Choose between Average or Median AQI for the heatmap"
    )
    
    # Filter data based on metric selection
    metric_data = monthly_data[monthly_data['metric'] == metric_selector]
    
    # Get all cities
    all_cities = metric_data['city'].unique()
    
    # Create a complete matrix for heatmap
    heatmap_matrix = []
    city_labels = []
    
    for city in all_cities:
        city_data = []
        city_labels.append(city)
        
        for month_name in month_order:
            # Find data for this city and month
            month_data = metric_data[
                (metric_data['city'] == city) & 
                (metric_data['month_name'] == month_name)
            ]
            
            if not month_data.empty:
                aqi_value = month_data['aqi_value'].iloc[0]
            else:
                aqi_value = np.nan  # Use NaN instead of None
            
            city_data.append(aqi_value)
        
        heatmap_matrix.append(city_data)
    
    # Convert to numpy array for heatmap
    heatmap_array = np.array(heatmap_matrix)
    
    # Handle text display - only show text for non-NaN values
    text_array = np.where(np.isnan(heatmap_array), '', np.round(heatmap_array, 1).astype(str))
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_array,
        x=month_order,
        y=city_labels,
        colorscale='Reds',
        text=text_array,
        texttemplate="%{text}",
        textfont={"size": 10},
        hoverongaps=False
    ))
    
    fig.update_layout(
        title=f'Monthly {metric_selector} AQI Heatmap - {selected_heatmap_year}',
        xaxis_title="Month",
        yaxis_title="City",
        height=400,
        width=None
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_summary_stats(df):
    """Create year-wise summary statistics"""
    st.markdown("## 📊 Year-wise Summary Statistics")
    
    if df.empty:
        st.warning("No data available for the selected filters.")
        return
    
    # Filter for available data only
    available_data = df[df['data_quality'] == 'available']
    
    if available_data.empty:
        st.warning("No available data for the selected filters.")
        return
    
    # Calculate year-wise summary statistics
    summary_stats = available_data.groupby(['city', 'year']).agg({
        'aqi_value': ['count', 'mean', 'std', 'min', 'max', 'median']
    }).round(2)
    
    # Flatten column names
    summary_stats.columns = ['Count', 'Mean', 'Std', 'Min', 'Max', 'Median']
    summary_stats = summary_stats.reset_index()
    
    # Add a comparison section for Average vs Median
    st.markdown("### 📊 Average vs Median AQI Comparison")
    
    # Calculate overall averages and medians by city
    city_comparison = available_data.groupby('city')['aqi_value'].agg(['mean', 'median']).round(1).reset_index()
    city_comparison.columns = ['City', 'Average AQI', 'Median AQI']
    city_comparison['Difference'] = city_comparison['Average AQI'] - city_comparison['Median AQI']
    
    st.dataframe(city_comparison, use_container_width=True)
    
    # Add explanation
    st.markdown("""
    **Note**: The difference between Average and Median AQI indicates the skewness of the data:
    - **Positive difference**: Data is right-skewed (more high AQI days)
    - **Negative difference**: Data is left-skewed (more low AQI days)
    - **Small difference**: Data is more symmetric
    """)
    
    # Sort by city and year
    summary_stats = summary_stats.sort_values(['city', 'year'])
    
    st.dataframe(summary_stats, use_container_width=True)

def create_data_table(df):
    """Create data table view"""
    st.markdown("## 📋 Raw Data Table")
    
    if df.empty:
        st.warning("No data available for the selected filters.")
        return
    
    # Show data table
    st.dataframe(
        df.sort_values(['city', 'date']),
        use_container_width=True,
        height=400
    )
    
    # Download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name=f"aqi_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

def main():
    """Main dashboard function"""
    # Create header
    create_header()
    
    # Load data
    df = load_data()
    summary = load_summary()
    
    if df.empty:
        st.error("❌ Failed to load data. Please check if the data files exist.")
        return
    
    # Create sidebar
    selected_cities, selected_years, date_range, aqi_range = create_sidebar()
    
    # Filter data
    filtered_df = filter_data(df, selected_cities, selected_years, date_range, aqi_range)
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 City Metrics", 
        "📈 Time Series", 
        "🏙️ City Comparison", 
        "📅 Monthly Analysis",
        "📋 Data Table"
    ])
    
    with tab1:
        create_city_metrics_section(filtered_df)
        create_summary_stats(filtered_df)
    
    with tab2:
        create_time_series_chart(filtered_df)
    
    with tab3:
        create_city_comparison_chart(filtered_df)
    
    with tab4:
        create_monthly_analysis(filtered_df)
    
    with tab5:
        create_data_table(filtered_df)

if __name__ == "__main__":
    main() 