function Table(tbl)
  if not tbl.head or not tbl.head.rows or #tbl.head.rows == 0 then
    return tbl
  end

  local header_texts = {}
  for _, cell in ipairs(tbl.head.rows[1].cells) do
    table.insert(header_texts, pandoc.utils.stringify(cell.content))
  end

  local is_sources_table = false
  for _, text in ipairs(header_texts) do
    if text == "url" or text == "URL" then
      is_sources_table = true
      break
    end
  end

  if is_sources_table and tbl.colspecs then
    local num_cols = #tbl.colspecs
    if num_cols >= 5 then
      for i = 1, num_cols - 1 do
        tbl.colspecs[i][1] = 'AlignLeft'
      end
      tbl.colspecs[num_cols][1] = 'AlignLeft'
    end
  end

  return tbl
end
