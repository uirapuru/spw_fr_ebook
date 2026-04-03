local function block_images(block)
  if block.t == "Figure" then
    for _, inner_block in ipairs(block.content) do
      if inner_block.t == "Plain" or inner_block.t == "Para" then
        for _, inline in ipairs(inner_block.content) do
          if inline.t == "Image" then
            return { inline }
          end
        end
      end
    end
    return nil
  end

  if block.t == "Para" then
    local images = {}
    for _, inline in ipairs(block.content) do
      if inline.t == "Image" then
        table.insert(images, inline)
      elseif inline.t == "SoftBreak" or inline.t == "LineBreak" or inline.t == "Space" then
        -- keep scanning
      else
        return nil
      end
    end

    if #images > 0 then
      return images
    end
  end

  return nil
end

local function set_width(img, width)
  img.attr.attributes["width"] = width
end

function Blocks(blocks)
  local i = 1
  while i <= #blocks do
    local imgs = block_images(blocks[i])
    if not imgs then
      i = i + 1
    else
      local j = i + 1
      local total_images = #imgs

      while j <= #blocks and block_images(blocks[j]) do
        total_images = total_images + #block_images(blocks[j])
        j = j + 1
      end

      local width = (total_images == 1) and "100%" or "90%"
      for k = i, j - 1 do
        local run_imgs = block_images(blocks[k])
        if run_imgs then
          for _, run_img in ipairs(run_imgs) do
            set_width(run_img, width)
          end
        end
      end
      i = j
    end
  end
  return blocks
end