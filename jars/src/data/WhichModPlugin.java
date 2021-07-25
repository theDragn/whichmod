package data;

import com.fs.starfarer.api.BaseModPlugin;
import com.fs.starfarer.api.Global;
import com.fs.starfarer.api.ModSpecAPI;
import com.fs.starfarer.api.SettingsAPI;
import com.fs.starfarer.api.combat.ShipHullSpecAPI;
import com.fs.starfarer.api.loading.Description;
import com.fs.starfarer.api.loading.Description.Type;
import com.fs.starfarer.api.loading.FighterWingSpecAPI;
import com.fs.starfarer.api.loading.HullModSpecAPI;
import com.fs.starfarer.api.loading.WeaponSpecAPI;
import org.apache.log4j.Level;
import org.apache.log4j.Logger;
import org.apache.log4j.Priority;
import org.jetbrains.annotations.Nullable;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

public class WhichModPlugin extends BaseModPlugin
{
    public static final String SETTINGS_FILE = "WHICHMOD_SETTINGS.json";

    public static final Map<String, String> modShortNameMap = new HashMap<>();
    public static boolean USE_FULL_NAMES;
    public static boolean EDIT_DESIGN;
    public static boolean SHIPS_AND_WEAPONS_ONLY;
    public static String LEFT_BRACKET;
    public static String RIGHT_BRACKET;
    private static Logger logger = Global.getLogger(WhichModPlugin.class);
    @Override
    public void onApplicationLoad() throws Exception
    {
        try
        {
            loadSettings();
        } catch (Exception e)
        {
            logger.log(Level.INFO, e.getMessage());
            // crash early and notify the user rather than allowing confusion
            throw new RuntimeException(
                    "WhichMod encountered a \"bruh moment\".\nAnd by that I mean there was an issue with the settings file."
            );
        }

        editDescriptions();
    }

    private void loadSettings() throws IOException, JSONException
    {
        JSONObject settings = Global.getSettings().loadJSON(SETTINGS_FILE);
        USE_FULL_NAMES = settings.getBoolean("useFullNames");
        EDIT_DESIGN = settings.getBoolean("editDesign");
        SHIPS_AND_WEAPONS_ONLY = settings.getBoolean("shipsAndWeaponsOnly");
        LEFT_BRACKET = settings.getString("bracketCharacterL");
        RIGHT_BRACKET = settings.getString("bracketCharacterR");

        JSONObject modIdData = settings.getJSONObject("modIDs");
        Iterator iter = modIdData.keys();
        while (iter.hasNext())
        {
            String id = (String) iter.next();
            String abbreviation = (String) modIdData.getString(id);
            modShortNameMap.put(id, abbreviation);
        }
    }

    private void editDescriptions()
    {
        SettingsAPI settings = Global.getSettings();
        List<ModSpecAPI> mods = settings.getModManager().getEnabledModsCopy();
        for (ModSpecAPI mod : mods)
        {
            JSONArray csvData;
            // try loading descriptions.csv; not every mod has one
            try
            {
                csvData = settings.loadCSV("data/strings/descriptions.csv", mod.getId());
            } catch (Exception e)
            {
                continue;
            }

            // try reading each row in descriptions.csv
            for (int i = 0; i < csvData.length(); i++)
            {
                try
                {
                    //System.out.println(csvData.get(i));
                    //logger.log(Priority.INFO, csvData.get(i));
                    JSONObject row = csvData.getJSONObject(i);
                    String id = row.getString("id");
                    String type = row.getString("type");
                    if (!(id == null || type == null || id.equals("") || type.equals("")))
                    {
                        Description desc;
                        Type descType = getType(type);
                        if ( descType == Type.SHIP || descType == Type.WEAPON)
                            desc = settings.getDescription(id, descType);
                        else if (descType != null && !SHIPS_AND_WEAPONS_ONLY)
                            desc = settings.getDescription(id, descType);
                        else
                            continue;

                        if (USE_FULL_NAMES || modShortNameMap.get(mod.getId()) == null)
                            desc.setText1(LEFT_BRACKET + mod.getName() + RIGHT_BRACKET + " "+ desc.getText1());
                        else
                            desc.setText1(LEFT_BRACKET + modShortNameMap.get(mod.getId()) + RIGHT_BRACKET + " " + desc.getText1());
                    }

                } catch (Exception e)
                {
                    logger.log(Level.INFO,"uh oh, stinky in " + mod.getId());
                    logger.log(Level.INFO, e);
                }
            }

        }
    }

    @Nullable
    public Type getType(String type)
    {
        switch (type)
        {
            case "SHIP":
                return Type.SHIP;
            case "WEAPON":
                return Type.WEAPON;
            case "ASTEROID":
                return Type.ASTEROID;
            case "SHIP_SYSTEM":
                return Type.SHIP_SYSTEM;
            case "CUSTOM":
                return Type.CUSTOM;
            case "ACTION_TOOLTIP":
                return Type.ACTION_TOOLTIP;
            case "FACTION":
                return Type.FACTION;
            case "PLANET":
                return Type.PLANET;
            case "RESOURCE":
                return Type.RESOURCE;
            case "TERRAIN":
                return Type.TERRAIN;
            default:
                return null;
        }
    }
}
