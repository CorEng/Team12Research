-- create tables to store all the data that from the database
-- the data type of this table based on the PDF

create table if not exists rt_trips(
    data_source varcharacter(4),
    day_of_service varcharacter (30),
    trip_id varcharacter(30),
    line_id varcharacter(10) default null,
    route_id varcharacter(20) default null,
    direction varcharacter(2) default null,
    planned_time_arrive INT default null,
    planned_time_departure INT default null,
    basin varcharacter(20) default null,
    tenderlot varcharacter(30) default null,
    actual_time_arrive INT default null,
    actual_time_departure INT default null,
    suppressed INT default null,
    justification_id INT default null,
    last_update varchar(30) default null,
    note varcharacter(255) default null,
    
    primary key (data_source, day_of_service, trip_id)
);

create table if not exists rt_vehicles(
    data_source varcharacter(4),
    day_of_service varcharacter(30),
    vehicle_id varcharacter(6),
    distance INT default null,
    minutes INT default null,
    last_update varchar(30),
    note varcharacter(255) default null,
    
    primary key (data_source, day_of_service, vehicle_id)
    
);

create table if not exists stops (
	stop_latitude float4,
	zone_id int,
	stop_longitude float4,
	stop_id varcharacter(20),
	stop_name varcharacter(255),
	location_type INT,
	
	primary key (stop_id)
);

create table if not exists rt_leave_times (
	data_source varcharacter(4),
	day_of_service varcharacter(30),
	trip_id varcharacter(30),
	progr_number INT,
	stop_point_id varcharacter(16) unique not null,
	planned_time_arrive INT default null,
	planned_time_departure INT default null,
	actual_time_arrive INT default null,
	actual_time_departure INT default null,
	vehicle_id varcharacter(6) default null,
	passengers INT default null,
	passengers_in INT default null,
	passengers_out INT default null,
	distance INT default null,
	suppressed int default null,
	justification_id INT default null,
	last_update varchar(30),
	note varcharacter(255) default null,
	
	primary key (data_source, day_of_service, trip_id, progr_number),
	foreign key (data_source, day_of_service, trip_id) references rt_trips (data_source, day_of_service, trip_id),
 	foreign key (data_source, day_of_service, vehicle_id) references rt_vehicles (data_source, day_of_service, vehicle_id),
	foreign key (stop_point_id) references stops (stop_id)
);

create table if not exists historical_weather( 
	station_id varcharacter(30) NOT NULL,
	longitude_degrees_east float4 DEFAULT NULL,
	latitude_degrees_north float4 DEFAULT NULL,
	time_UTC varcharacter(30) NOT NULL,
	atmospheric_pressure_mb float4 NOT NULL,
	wind_direction_true INT NOT NULL,
	wind_speed_kn float4 NOT NULL,
	gust_kn float4 NOT NULL,
	wave_height_m INT,
	wave_periods INT,
	mean_wave_direction_true INT,
	h_max float4,
	air_temperature_degree_C float4,
	dew_point_degree_C float4,
	sea_temperature_degree_C float4,
	relative_humidity_percent float4,
	QC_flag INT,
	
	primary key(station_id, time_UTC)	  
	
);