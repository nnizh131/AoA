from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

def get_data_per_anchor(df, anchor):
    return df.loc[df['anchor'] == anchor]

def spatial_plot(errors, location_x, location_y, filename, title, testing_room='testbench_01_furniture_mid_concrete', mode='xy', vmin=None, vmax=None, cmap='PuBu'):

    """
    Error per point plot
    """
    errors = pd.DataFrame({

    'coord_x': location_x,

    'coord_y':location_y,

    'errors': errors,

    })
    # errors['xy'] = preds- true_pos
    # errors[['xy']] = true_pos
    # errors['xy'] = mean_absolute_error(preds, true_pos)
    # errors[['x_tag', 'y_tag', 'z_tag']] = true_pos
    ax = plt.gca()
    mappable = errors.plot.hexbin('coord_x', 'coord_y', 'errors', gridsize=(35,12), figsize = (17,7), cmap=cmap, vmin=vmin, vmax=vmax, ax=ax)
    addFurniture(ax, testing_room)
    ax.set_xlabel('x(m)')
    ax.set_ylabel('y(m)')
    ax.set_ylim(43,50.3)
    ax.set_xlim(43.9,58.2)
    ax.set_xticklabels(list(range(-2,15,2)))
    ax.set_yticklabels(list(range(0,8)))
    ax.text(60.3, 46, 'MAE (angle)', rotation=90)
    ax.set_title(title)
    plt.savefig(filename,bbox_inches='tight', pad_inches = 0)
    plt.show()

def addFurniture(ax, room, anchors=[1,2,3,4]):

    """
    Adds furniture in spatial plot
    """

    a = np.array([1,1,1,1,1,1])
    a_low = 0.5
    if room in ['testbench_01_furniture_mid', 'testbench_01_furniture_mid_concrete']:
        a[1] = a[3] = a_low
    if room in ['testbench_01_furniture_low', 'testbench_01_furniture_low_concrete']:
        a[2] = a[0] = a_low
    if room in ['testbench_01', 'testbench_01_scenario2', 'testbench_01_scenario3']:
        a = 6*[a_low]
    furniture = [plt.Rectangle((44.+1.9, 43.1+0.2), 0.5, 1, fc='orange', ec='black', lw=2, alpha=a[0]),
                 plt.Rectangle((44.+4.45, 43.1+1), 0.5, 1, fc='orange', ec='black', lw=2, alpha=a[1]),
                 plt.Rectangle((44.+6.4, 43.1+2.6), 0.5, 1, fc='orange', ec='black', lw=2, alpha=a[2]),
                 plt.Rectangle((44.+1.7, 43.1+4.1), 0.5, 1, fc='orange', ec='black', lw=2, alpha=a[3]),
                 plt.Rectangle((44.+4.2, 43.1+3.4), 0.5, 1, fc='orange', ec='black', lw=2, alpha=a[4]),
                 plt.Rectangle((44.+5.4, 43.1+5.15), 0.5, 1, fc='orange', ec='black', lw=2, alpha=a[5]),]
    
    anchrs = [plt.Circle((57.9, 43.3), 0.2, fc='firebrick', ec='black', lw=2),
               plt.Circle((57.9, 50.0), 0.2, fc='firebrick', ec='black', lw=2),
               plt.Circle((44.3, 50.0), 0.2, fc='firebrick', ec='black', lw=2),
               plt.Circle((44.3, 43.3), 0.2, fc='firebrick', ec='black', lw=2)]

    for anchor in anchors:
        ax.add_patch(anchrs[anchor-1])
    for item in furniture:
        ax.add_patch(item)