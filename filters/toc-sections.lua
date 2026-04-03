local category_markers = {
  ["Su-24M"] = "Lotnictwo",
  ["Geran-2 (Shahed-136)"] = "Drony bojowe (BSP)",
  ["Czołg średni T-55"] = "Czołgi",
  ["BMD-1"] = "Bojowe Wozy Desantowe (BWD)",
  ["Bojowy Wóz Piechoty BMP-1"] = "Bojowe Wozy Piechoty (BWP)",
  ["MT-LB"] = "Transportery opancerzone (APC)",
  ["2S19 Msta-S"] = "Artyleria samobieżna",
  ["Haubica holowana D-30"] = "Artyleria holowana",
  ["ZU-23-2"] = "Systemy przeciwlotnicze",
  ["Przeciwpancerny pocisk kierowany 9K111 Fagot"] = "Przeciwpancerne pociski kierowane (ATGM)",
  ["Karabin szturmowy AK-74"] = "Karabiny szturmowe",
  ["Ręczny karabin maszynowy RPK"] = "Karabiny maszynowe",
  ["Karabin snajperski VSS Wintorez"] = "Karabiny snajperskie",
  ["Granatnik przeciwpancerny RPG-7"] = "RPG i wyrzutnie rakietowe",
  ["Nasadkowy granatnik GP-25 Kostior"] = "Wyrzutnie granatów",
  ["Pistolet Makarowa PM"] = "Pistolety i pistolety maszynowe",
  ["Granat ręczny F-1"] = "Granaty ręczne",
  ["Mina przeciwpiechotna PMN"] = "Miny",
}

local inserted = {}

local function starts_with(text, prefix)
  return text:sub(1, #prefix) == prefix
end

function Header(el)
  if el.level ~= 1 then
    return nil
  end

  local title = pandoc.utils.stringify(el.content)
  for prefix, category in pairs(category_markers) do
    if not inserted[category] and starts_with(title, prefix) then
      inserted[category] = true
      return {
        pandoc.RawBlock("latex", "\\phantomsection\\addcontentsline{toc}{sectionheader}{" .. category .. "}"),
        el,
      }
    end
  end

  return nil
end