
plot_layout = dict(
    dragmode="select",
    autosize=True,
    automargin=True,
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    font=dict(color="#777777"),
)

GAS_COLORS = dict(
    CO2="#3690C0",
    CH4="#F87A72",
    CO="#ABD9E9",
    H2="#A1D99B",
    C2H4="#BFD3E6",
    C2H6="#B3DE69",
    C3H8="#FDBF6F",
    N2="#FC9272",
    O2="#D4B9DA",
    CH3OH="#FA9FB5"
)

APPLICATIONS = {
    #FORMAT {'appID': 'User Friendly Label'}
    'Vehicle': 'Electric Vehicles',
    'Mobility': 'Electric Mobililty',
    'Marine': 'Marine Applications',
    'Remote': 'Remote Control Devices',
    'Robotics': 'Robotics',
    'Storage': 'Energy Storage',
    'Electronics': 'Personal Electronics',
    'Consumer': 'Consumer Devices',
    'Backup': 'Battery Backup',
    'Tools': 'Power Tools',
    'Medical': 'Medical Devices',
    'Post-Life': 'Post-Life',
    'Production': 'Battery Manufacturing',
    'Smoking': 'E-Cigarettes',
    'Toys': 'Toys',
    'Unknown': 'Unknown'
}

INCIDENTS = {
    #FORMAT {'Internal String': 'External Label'}
    'Cell Failure': 'Cell Failure',
    'Fire': 'Fire',
    'Explosion': 'Explosion'
}
